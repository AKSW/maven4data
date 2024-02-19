---
title: Maven Polyglot
layout: default
parent: How-Tos
nav_order: 15
---

# Maven Polyglot


## Synopsis

Maven Polyglot allows one to write a `pom` in other formats than XML.
Supported languages include YAML, JSON, or even Ruby.

## Purpose

XML is quite verbose. Its popularity declined with the advent of newer formats such as YAML.

## Limitations

For specific issues, it may be more likely to find solutions using XML rather than any other format.

## Notes

* Polyglot translates non-XML builds into the abstract project object model (pom) which can be serialized as XML again.
* When deploying a polyglot project, only the XML model is deployed. This ensures interoperability with any existing
XML-based pipelines.
* Deploying a polyglot pom file can be done by [attaching it as an artifact](attaching-artifacts.md).

## Enabling Polyglot

In order to use Polyglot, you need to tell maven to load the polyglot extension prior to starting the actual build.

In your project, create (or update) the file `.mvn/extensions.xml` with the following content:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<extensions>
    <extension>
        <groupId>io.takari.polyglot</groupId>
        <artifactId>polyglot-yaml</artifactId>
        <version>0.7.0</version>
    </extension>
</extensions>
```

## Example

Now you can create e.g. a `pom.yml` with the following content.
The example is a YAML version of [How To Archive a Directory](archive-a-directory.md).

```yml
modelVersion: 4.0.0
groupId: org.aksw.maven4data.examples
artifactId: my-archived-directory-polyglot
version: 0.0.1-SNAPSHOT
name: 'Package a directory in YAML'

properties:
  directory-to-archive: .
  project.build.sourceEncoding: UTF-8
  
build:
  resources:
    - directory: ${directory-to-archive}
```

## Validation

* As usual, you can validate a pom file using:

```
mvn validate
```

* For debugging it is often helpful to convert the YAML to JSON first. The tool `yq` can be used for this purpose:

```bash
yq -o json -p yaml pom.yml
```

## Ployglot Quick Links

* Latest versions: [https://search.maven.org/search?q=io.takari.polyglot](https://search.maven.org/search?q=io.takari.polyglot)
* Supported languages: [https://github.com/takari/polyglot-maven#available-languages](https://github.com/takari/polyglot-maven#available-languages)
* Examples: [https://github.com/takari/polyglot-maven-examples](https://github.com/takari/polyglot-maven-examples)


