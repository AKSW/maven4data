---
title: Archiving Code and Data
layout: default
nav_order: 35
---

# Archiving Resources 

## Synopsis

This chapter shows how any folder can be quickly archived as a versioned maven artifact.

## Purpose

* Package up scrips and resources (e.g. datasets) as maven artifacts that can be used in downstream build pipelines.
For example, in the [Build anything with Docker](build-anything-with-docker.md) chapter, a JAR bundle with python resources is extracted for building the docker image.

## Approach

The following `pom.xml` is self-contained.
The jar bundle can be built with

```bash
mvn package
```

It adds the current folder and its sub folders recursively to the jar file in the target folder.
Adjust the `folder` property to a meaningful folder of your project such as `src`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.aksw.maven4data.examples</groupId>
  <artifactId>archive-folder</artifactId>
  <version>1.0.0-SNAPSHOT</version>

  <!-- JAR files are ZIP files, so we are actually just creating a ZIP file here -->
  <packaging>jar</packaging>

  <properties>
    <!-- Adjust the path to your needs -->
    <folder>.</folder>

    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <!-- Include the specified folder as a resource. Its contents will be added to the root of the JAR bundle. -->
  <build>
    <resources>
      <resource>
        <directory>${folder}</directory>
      </resource>
    </resources>
  </build>
</project>
```


### Another Example

The following is a more realistic example of a project structure:

```
|- README.md
|- src
|  |- requirements.txt
|  |- run.sh
|  +- LICENSE.txt
|
|- LICENSE.txt # symlink to src/LICENSE.txt
|- pom.xml
|
| # The build output created with "mvn package":
+- target
   +- archive-folder-1.0.0-SNAPSHOT.jar
```

By setting the `folder` property to `src` in the above `pom.xml`, the content of the `src` folder up at the root of the versioned JAR file.

