import feedparser
import json
import requests
from dateutil.parser import parse
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import XSD, RDFS, RDF
import xml.etree.ElementTree as ET
from tqdm import tqdm
import fsspec
import time

CACHE_DIR = "/tmp/coypu/semscron/disasters_polygon_file_cache"
COY_COUNTRY_NS = "https://data.coypu.org/country/"

coy = Namespace("https://schema.coypu.org/global#")
geo = Namespace("http://www.opengis.net/ont/geosparql#")
emdat = Namespace("https://schema.coypu.org/em-dat#")

def get_gdacs_events():
    url = "https://www.gdacs.org/xml/rss.xml"
    return feedparser.parse(url).entries


def get_reliefweb_events():
    url = "https://api.reliefweb.int/v1/disasters?appname=coypu&profile=full&preset=latest&slim=1&limit=100"
    return json.loads(requests.get(url).content)['data']


def add_coordinates(iri, lat, lon, graph):
    geo_iri = iri + "/geometry"
    graph.add((geo_iri, RDF.type, geo.Geometry))
    graph.add((geo_iri, geo.asWKT, Literal(f"Point({lon} {lat})", datatype=geo.wktLiteral)))
    graph.add((iri, geo.hasGeometry, geo_iri))
    
    graph.add((iri, URIRef(coy.hasLatitude), Literal(lat, datatype=XSD.float)))
    graph.add((iri, URIRef(coy.hasLongitude), Literal(lon, datatype=XSD.float)))
    
    return graph


namespaces = {'tc': 'urn:oasis:names:tc:emergency:cap:1.2',
              'gdacs': 'http://www.gdacs.org'}


def get_gdacs_affected_countries(event_iri: URIRef, item) -> Graph | None:
    # impact is only available in the event RSS feed
    event_rss_url = item['gdacs_resource']['url']

    if event_rss_url is not None:
        time.sleep(1)
        with fsspec.open(
               f"filecache::{event_rss_url}",
                filecache={'cache_storage': CACHE_DIR}
        ) as f1:
            root = ET.fromstring(f1.read())

            impact_xml_elt = root.find(".//gdacs:resource[@id = 'impact_xml']", namespaces)

            if impact_xml_elt is not None:
                impact_xml_url = impact_xml_elt.attrib['url']\
                    .replace('%5C', '/').replace('\\', '/')

                if impact_xml_url is not None:
                    print(f"loading impact XML feed from {impact_xml_url}")
                    time.sleep(1)
                    with fsspec.open(
                           f"filecache::{impact_xml_url}",
                            filecache={'cache_storage': CACHE_DIR}
                    ) as f2:
                        root = ET.fromstring(f2.read())

                        graph = Graph()

                        for iso3 in root.findall(".//datums[@alias = 'country']/datum[type = 'country']//scalar[name = 'ISO_3DIGIT']/value"):
                            graph.add((event_iri, coy.hasCountryLocation, URIRef(COY_COUNTRY_NS + iso3.text)))

                        return graph


def create_gdacs_affected_regions_wkt(event_iri: URIRef, item, merge_polygons: bool = True) -> Graph:
    """
    Gets the area information of GDACS events if available. The polygons itself are serialized as WKT strings.
    The data is fetched via using the 'gdacs:cap' element of the given event feed element. This leads to another XML
    file which does contain one or more <area> elements containing the polygons.
    The generated RDF data does match the GeoSPARQL standard, i.e.
    for a given event we attach an 'affectedRegion' and this region has the geometry with the WKT literal as
    serialization:

    Example:
    ---------
    :event coy:hasAffectedRegion :event/area .
    :event/area geo:hasGeometry :event/area/geom .
    :event/area/geom geo:asWKT "POLYGON (( ))" .


    :param event_iri: the event rdflib IRI object
    :param item: the XML feed item
    :param merge_polygons: whether to merge multiple polygons into a single WKT "MULTIPOLYGON" object instead of
    multiple WKT "POLYGON" objects.
    :return: the RDF graph object
    """
    cap = item['gdacs_cap']

    if cap is not None:

        with fsspec.open(
               f"filecache::{cap}",
                filecache={'cache_storage': CACHE_DIR}
        ) as f:
            root = ET.fromstring(f.read())

            for info in root.findall('tc:info', namespaces):

                graph = Graph()

                polygons = []

                for area in info.findall('tc:area', namespaces=namespaces):
                    if area is not None:
                        for idx, polygon_node in enumerate(area.findall('tc:polygon', namespaces=namespaces)):
                            polygon = polygon_node.text

                            xy_pairs = polygon.split(" ")
                            xy_pair_splits = [xy.split(",") for xy in xy_pairs]
                            wkt_point_pairs = [f"{split[1]} {split[0]}" for split in xy_pair_splits]
                            wkt_polygon = "POLYGON((" + ", ".join(wkt_point_pairs) + "))"

                            polygons.append(wkt_polygon)

                if merge_polygons and len(polygons) > 1:
                    n_chars = len("POLYGON")
                    polygons = ["MULTIPOLYGON(" + ",".join([p[n_chars:] for p in polygons]) + ")"]

                for idx, polygon in enumerate(polygons):
                    region_iri = URIRef(str(event_iri) + "/area" + ("/" + str(idx) if len(polygons) > 1 else ""))
                    graph.add((event_iri, coy.hasAffectedRegion, region_iri))
                    region_geom = URIRef(str(region_iri) + "/geometry")
                    graph.add((region_iri, geo.hasGeometry, region_geom))
                    graph.add((region_geom, geo.asWKT, Literal(polygon, datatype=geo.wktLiteral)))

                return graph


gdacs_polygon_api_url = "https://www.gdacs.org/gdacsapi/api/polygons/getgeometry"
def get_gdacs_polygon(event_id, event_type, episode_id):
    query = {'eventtype': event_type, 'eventid': event_id, 'episodeid': episode_id}
    # response = requests.get(gdacs_polygon_api_url, params=query)

    url = f"{gdacs_polygon_api_url}?" + "&".join([f"{k}={v}" for k, v in query.items()])
    with fsspec.open(
            f"blockcache::{url}",
            blockcache={"cache_storage": "cache"}
    ) as f:
        geojson = json.loads(f.read())

        return geojson


def create_gdacs_affected_regions_geojson(event_iri: URIRef, feed_item) -> Graph:
    # rss_resource = feed_item['gdacs_resource']
    # event_rss = feedparser.parse(rss_resource['url'])
    #
    # # check for GeoJSON file
    # event_item = event_rss.entries[0]
    # resources = event_item['gdacs_resources']
    # for r in resources:
    #     if r.id == "dynamic_map_event":
    #         print(r['title'])
    geojson = get_gdacs_polygon(event_id=feed_item['gdacs_eventid'],
                                event_type=feed_item['gdacs_eventtype'],
                                episode_id=feed_item['gdacs_episodeid'])

    graph = Graph()

    region_iri = URIRef(str(event_iri) + "/area")
    graph.add((event_iri, coy.hasAffectedRegion, region_iri))
    region_geom = URIRef(str(region_iri) + "/geometry")
    graph.add((region_iri, geo.hasGeometry, region_geom))
    graph.add((region_geom, geo.asGeoJSON, Literal(json.dumps(geojson), datatype=geo.geoJSONLiteral)))

    return graph


EMDAT = Namespace("https://schema.coypu.org/em-dat#")
EMDAT_URL = "https://gitlab.com/coypu-project/coy-ontology/-/raw/main/ontology/events/em-dat.ttl"


def get_emdat_ontology() -> Graph:
    g = Graph()
    g.parse(EMDAT_URL, format="turtle")
    return g


event_type_mapping = {}
g = get_emdat_ontology()
for emdat_cls, p, glide in g.triples((None, EMDAT.hasGlideHazardCode, None)):
    event_type_mapping[str(glide)] = {"cls": emdat_cls}


gdacs_event_type_mapping = {
    "TC": {"name": "Tropical Cyclone", "cls": EMDAT.TropicalCyclone},
    "TS": {"name": "Tsunami", "cls": EMDAT.Tsunami},
    "EQ": {"name": "Earthquake", "cls": EMDAT.Earthquake},
    "FL": {"name": "Flood", "cls": EMDAT.Flood},
    "VO": {"name": "Volcano", "cls": EMDAT.VolcanicActivity},
    "WF": {"name": "Wildfire", "cls": EMDAT.Wildfire},
    "DR": {"name": "Drought", "cls": EMDAT.Drought},
}


def create_gdacs_graph(graph: Graph, show_progress: bool = False):
    base_iri = "https://data.coypu.org/event/gdacs/"
    country_iri = "https://data.coypu.org/country/"
    
    events = get_gdacs_events()

    pbar = tqdm(events, disable=not show_progress)
    for idx, event in enumerate(pbar):
        id = event['id']
        iri = URIRef(base_iri + str(id))
        pbar.set_description("Processing %s" % id)
        
        graph.add((iri, RDF.type, coy.Disaster))
        graph.add((iri, RDF.type, coy.Event))
        # add EM-Dat event type class
        event_type = event['gdacs_eventtype']
        event_type_cls = event_type_mapping[event_type]['cls']
        if event_type_cls is not None:
            graph.add((iri, RDF.type, event_type_cls))
        graph.add((iri, RDFS.label, Literal(event['title'], lang='en')))
        graph.add((iri, RDFS.comment, Literal(event['summary'], lang='en')))
        graph.add((iri, coy.hasUrl, Literal(event['links'][1]['href'], datatype=XSD.anyURI)))
        
        graph.add((iri, coy.hasPublicationTimestamp, Literal((str(parse(event['published'])).replace(" ", "T")), datatype=XSD.dateTime)))
        graph.add((iri, coy.hasStartTimestamp, Literal((str(parse(event['gdacs_fromdate'])).replace(" ", "T")), datatype=XSD.dateTime)))
        
        if event['gdacs_iscurrent'] == 'true':
            graph.add((iri, coy.hasCurrentTimestamp, Literal((str(parse(event['gdacs_todate'])).replace(" ", "T")), datatype=XSD.dateTime)))
            graph.add((iri, coy.hasEventStatus, Literal("Current", lang='en')))
        else:
            graph.add((iri, coy.hasEndTimestamp, Literal((str(parse(event['gdacs_todate'])).replace(" ", "T")), datatype=XSD.dateTime)))
            graph.add((iri, coy.hasEventStatus, Literal("Past", lang='en')))
        
        graph.add((iri, coy.hasEventType, Literal(event['gdacs_eventtype'], lang='en')))
        graph.add((iri, coy.hasAlertScore, Literal(event['gdacs_alertscore'], datatype=XSD.decimal)))
        graph.add((iri, coy.hasAlertLevel, Literal(event['gdacs_alertlevel'], lang='en')))
        graph.add((iri, coy.hasAffectedPopulation, Literal(event['gdacs_population']['value'], datatype=XSD.decimal)))

        add_coordinates(iri, lat=event['geo_lat'], lon=event['geo_long'], graph=graph)

        iso3 = event['gdacs_iso3']
        if iso3 != '':
            graph.add((iri, coy.hasCountryLocation, URIRef(country_iri + iso3)))

        affected_countries_graph = get_gdacs_affected_countries(iri, event)
        if affected_countries_graph is not None:
            graph += affected_countries_graph

        # add triples that map the polygons for affected regions
        time.sleep(3) # wait 500ms to avoid being blocked for too many requests
        area_graph = create_gdacs_affected_regions_wkt(iri, event)
        if area_graph is not None:
            graph += area_graph

        # time.sleep(0.5)
        # area_graph = create_gdacs_affected_regions_geojson(iri, event)
        # if area_graph is not None:
        #     graph += area_graph

        # if idx == 10:
        #     break
    
    return graph


def create_reliefweb_graph(graph: Graph):
    base_iri = "https://data.coypu.org/event/reliefweb/"
    country_iri = "https://data.coypu.org/country/"
    
    events = get_reliefweb_events()

    for event in events:
        id = event['id']
        iri = URIRef(base_iri + str(id))

        graph.add((iri, RDF.type, coy.Disaster))
        graph.add((iri, RDF.type, coy.Event))

        fields = event['fields']

        # add EM-Dat event type class
        event_type = fields['primary_type']['code']
        event_type_cls = event_type_mapping[event_type]['cls']
        if event_type_cls is not None:
            graph.add((iri, RDF.type, event_type_cls))

        graph.add((iri, RDFS.label, Literal(fields['name'], lang='en')))
        graph.add((iri, RDFS.comment, Literal(fields['description'], lang='en')))
        graph.add((iri, coy.hasUrl, Literal(fields['url_alias'], datatype=XSD.anyURI)))

        graph.add((iri, coy.hasPublicationTimestamp, Literal(fields['date']['created'], datatype=XSD.dateTime)))
        graph.add((iri, coy.hasEventType, Literal(fields['primary_type']['code'], lang='en')))
        graph.add((iri, coy.hasEventStatus, Literal(str(fields['status'].capitalize()), lang='en')))

        if fields['status'] == 'ongoing':
            graph.add((iri, coy.hasStartTimestamp, Literal(fields['date']['event'], datatype=XSD.dateTime)))
            graph.add((iri, coy.hasCurrentTimestamp, Literal(fields['date']['changed'], datatype=XSD.dateTime)))
        elif fields['status'] == 'alert':
            graph.add((iri, coy.hasStartTimestamp, Literal(fields['date']['event'], datatype=XSD.dateTime)))
            graph.add((iri, coy.hasEndTimestamp, Literal(fields['date']['event'], datatype=XSD.dateTime)))
        else:
            graph.add((iri, coy.hasStartTimestamp, Literal(fields['date']['event'], datatype=XSD.dateTime)))
            graph.add((iri, coy.hasEndTimestamp, Literal(fields['date']['changed'], datatype=XSD.dateTime)))

        add_coordinates(iri,
                        lat=fields['primary_country']['location']['lat'],
                        lon=fields['primary_country']['location']['lon'],
                        graph=graph)
        graph.add((iri, coy.hasCountryLocation, URIRef(country_iri + str(fields['primary_country']['iso3']).upper())))

        # if enabled, add also the other affected country locations
        if 'country' in fields:
            countries = fields['country']
            for country in countries:
                graph.add(
                    (iri, coy.hasCountryLocation, URIRef(country_iri + str(country['iso3']).upper())))
    
    return graph

import click


@click.command()
@click.option('-o', '--output', type=click.Path(writable=True), default='disasters.nt', help='Output N-Triples file')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Show progress.')
def run(output, verbose: bool):
    graph = Graph()

    graph.bind('coy', coy)
    graph.bind('geo', geo)
    graph.bind('emdat', emdat)
    graph.bind("gdacs", Namespace("https://data.coypu.org/event/gdacs/"))
    graph.bind("reliefweb", Namespace("https://data.coypu.org/event/reliefweb/"))

    create_gdacs_graph(graph, verbose)
    create_reliefweb_graph(graph)

    with open(output, 'w') as file:
        file.write(graph.serialize(format='nt'))
    # file.write(graph.serialize(format='nt'))


if __name__ == '__main__':
    run()
