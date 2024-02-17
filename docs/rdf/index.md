---
title: Processing RDF
layout: default
nav_order: 50
---

## Processing RDF with Maven

### Summary

This chapter introduces the `sparql-maven-plugin`.

### Purpose

* The plugin enables within a `pom.xml` file the generate, transformation, enrichment, and repair of any type of RDF data. 
* What makes the combination of SPARQL and Maven especially powerful is the interplay of maven properties with SPARQL:
  * Maven metadata can be used to interpolate SPARQL query strings.
  * Conversely, SPARQL function extensions make it possible to query the `pom.xml` model using XPath.

### Use Cases

* The `maven-sparql-plugin` is a powerful tool that can be used for many use cases. A typical use case is to generate metadate in the following models:
  * Vocabulary of Interlinked Datasets (VoID): Captures statistical information about an RDF dataset, such as the frequences of classes and properties.
  * Provenance Ontology (PROV-O): Can be used to capture the plan that was used to produced a dataset - with the maven4data paradigm this plan is the `pom.xml` file -
    which can be referenced by its maven coordinate!
  * Data Catalog (DCAT) Vocabulary: Captures versions, publishers and distributions (= means of access) of a dataset.

### Limitations

* Currently the SPARQL functions do not support generating the *effective* `pom.xml`. This is future work and a contribution would be welcome.


### Basic Approach
TODO Adapt and test example.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.aksw.data.config</groupId>
  <artifactId>dcat-generator</artifactId>
  <version>0.0.1-SNAPSHOT</version>

  <properties>
    <input.url>pom.xml</input.url>

    <output.type>ttl.bz2</output.type>
    <output.classifier>dcat</output.classifier>
    <output.path>${project.build.directory}/${project.artifactId}-${output.classifier}.${output.type}</output.path>
    
    <description>This description is shared between maven and SPARQL.</description>
  </properties>

  <descriptions>${description}</description>

  <build>
    <plugins>
      <plugin>
        <groupId>org.aksw.maven.plugins</groupId>
        <artifactId>sparql-maven-plugin</artifactId>
        <version>0.0.1-SNAPSHOT</version>
        <executions>
          <execution>
            <id>generate-metadata</id>
            <phase>process-resources</phase>
            <goals>
              <goal>run</goal>
            </goals>
            <configuration>
              <!-- TDB2 is a disk-based engine. When engine is omitted, then the in-memory one will be used -->
              <engine>tdb2</engine>
              <outputFile>${output.path}</outputFile>
              <outputFormat>${output.type}</outputFormat>
              <env>
                <DATASET>${input.urn.dataset}</DATASET>
                <BASE>${input.urn.base}#</BASE>
                <POM>${input.pom.path}</POM>
              </env>
              <args>
                <!-- -->
                <arg>${input.data.path}</arg>

                <arg>void/sportal/compact/qb2.rq</arg>

<!-- A construct query string whose property references are interpolated before the query is evaluated -->
<arg><![CDATA[
CONSTRUCT {
  <urn:mvn:${groupId}:${artifactId}:${version}#dataset>
    a dcat:Dataset ;
    rdfs:comment """${description}"""@en ;
    .
}
WHERE {
}
]]></arg>
                
              </configuration>
            </execution>
          </executions>
      </plugin>
    </plugins>
  </build>
</project>

```


