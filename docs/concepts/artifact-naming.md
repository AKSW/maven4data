---
title: Artifact Naming
layout: default
parent: Concepts
nav_order: 20
---

## Artifact Naming

Artifacts in Maven are located along a 5 dimensional coordinate system.

The three most fundamental fields are:

* `groupId`
* `artifactId`
* `version`

These fields are often also referred to as the **GAV**.

* The groupId is typically a domain name such as `org.myorganization.mydepartment.myproject` and can thus be used to link an artifact to an organization in a Web-compatible way.
* The artifactId is used as the name of a relevent unit of work within the group.
* The version naturally is an identifier to capture a "snapshot" of that unit of work a certain point in time.

The remaining two fields are:

* `type`: The type of the artifact. Usually a filename extension such as `jar`, `zip` or `nt.bz2`.
  As a Java-centric convention, if the type is left empty then it **defaults to `jar`**. So there is no "empty" type.
* `classifier`: A custom string to discriminate further files published under the same GAV.

### Syntax

Maven coordinates are usually represented with the syntax:

```
groupId:artifactId:version[:type[:classifier]]
```

The `[]` indicate optional fields, so type and classifier may be omitted, but if a classifier is needed, then a type must be given as well.

Obviously colons (`:`) must not be used within values for any of the fields.

See Maven's [Guide to naming conventions](https://maven.apache.org/guides/mini/guide-naming-conventions.html) for details about how to choose proper values and the valid characters.

### Maven Coordinates, Files and Relative URLs

Maven coordinates can be unambigiously mapped to directory names and file names. These in turn correspond to relative URLs:

* The `groupId` is turned into a directory prefix by replacing all `.` with `/`:
* A filename is derived as follows:
  * If the classifier is absent, then the pattern is `artifactId-[version].[type]`.
  * Otherwise it is, `artifactId-[version]-[classifier].[type]`

Example without classifier. Lets assume a monthly report is published as a PDF file.
* Coordinate:    `org.example:report:2024.02.01:pdf`:
* Translates to: `org/example/report-2024.02.01.pdf`


Example with classifier. Let's assume a monthly report includes multiple files for different aspects such as sales.
* Coordinate:    `org.example:report:2024.02.01:pptx:sales`:
* Translates to: `org/example/report-2024.02.01-sales.pptx`

### Resolution of Maven Coordinates

A maven artifact's byte sequence is made accessible by forming an absolute URL from a repository's base URL with the artifacts relative URL.

* Resolving `org.aksw.data.config.aksw-data-deployment:aksw-data-deployment:0.0.8:pom`
* against `https://repo1.maven.org/maven2/`
* yields https://repo1.maven.org/maven2/org/aksw/data/config/aksw-data-deployment/0.0.8/aksw-data-deployment-0.0.8.pom

### Maven Coordinates and URNs

While there is no official URN scheme for maven coordinates, they are naturally suitable for that purpose.

In maven4data we use the prefix `urn:mvn:` to build urns such as `urn:mvn:org.example:report:2024.02.01:pdf`.

### Maven URNs and the Semantic Web

Maven URNs are suitable for direct use with RDF. The following example is valid RDF:

```
PREFIX dcat: <http://www.w3.org/ns/dcat#>

<urn:mvn:org.example:report:2024.02.01:pdf#distribution>
  dcat:downloadURL <urn:mvn:org.example:report:2024.02.01:pdf>  .
```

Now, it may not seem ideal to use a URN as a value of a property demanding a URL.
The point is, that from this RDF document we can devise a simple transformation procedure to turn some or all URNs into resolvable HTTPS URLs!
A simple build step can now be used to adjust the initial RDF document to create a version with actual download URLs.
We may for example want to resolve all maven URNs that appear as values of `dcat:downloadURL` against `https://my.domain/files/`. The result is:


```
PREFIX dcat: <http://www.w3.org/ns/dcat#>

<urn:mvn:org.example:report:2024.02.01:pdf#distribution>
  dcat:downloadURL <https://my.domain/files/org/example/report/report-2024.02.01.pdf>  .
```



