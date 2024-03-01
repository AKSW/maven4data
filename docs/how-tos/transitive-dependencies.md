---
title: Transitive Data Dependencies
layout: default
parent: How-Tos
nav_order: 50
---

# Transitive Data Dependencies

## Synopsis

This document explains how to create publish data artifacts with dependencies and how to resolve
the dependencies transitively in a consumer project.

## Purpose

Maven's `default` life cycle runs several maven plugins that implement conventions for how to process dependencies of type `jar`.
For example, the `maven-compiler-plugin` will add all jar files to the build path such that compilation of the source
code will detect when referenced classes and methods do not exist.

However, non-jar dependencies are not automatically handled.
This may give rise to the misconception that Maven cannot handle non-Java artifacts.
In reality, non-jar dependencies are resolved and downloaded into the local repository as usual.
Its just that there are no conventions for what to do with those dependencies afterwards.

For example, consider dependencies of type `csv`.
Should they be copied to the build output directory?
Do they need to go into e.g. the `META-INF` folder?
Or maybe we need to process the csv files first?

Depending on your use case, any option is reasonable.
So we need to provide our own rules about what to do with those artifacts.

## Publishing Data Artifacts

You need two modules for this purpose:

* Create a *publisher* `pom.xml` that attaches the data files
* Create a *aggregator* `pom.xml` that declares the coordinates of the published files as dependencies.

As publisher and aggregator are coupled, you may want to create a parent `pom.xml` that declares
them both as modules.

Note: It seems its not possible to combine publisher and aggregator into the same pom,
because dependencies are resolved before the attachment -
effectively causing the dependency resolution will fail.

## Copying Data Dependencies to a Directory

We can leverage the `maven-dependencies-plugin:copy-dependencies` goal in conjunction with the `<includeTypes>`
configuration option to copy any (transitive!) dependency of a certain type to a specific directory.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>org.aksw.data.config</groupId>
    <artifactId>aksw-data-deployment</artifactId>
    <version>0.0.8</version>
    <relativePath></relativePath>
  </parent>

  <groupId>org.aksw.data.gtfsbench</groupId>
  <artifactId>gtfsbench-rdf-1-consumer</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <packaging>pom</packaging>

  <properties>
    <data.workdir>${project.build.directory}/resources</data.workdir>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.aksw.data.gtfsbench</groupId>
      <artifactId>gtfsbench-csv-1-deps</artifactId>
      <version>0.0.1-SNAPSHOT</version>
      <type>pom</type>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-dependency-plugin</artifactId>
        <version>3.6.1</version>
        <executions>
          <execution>
            <id>copy-resource-dependencies</id>
            <phase>generate-resources</phase>
            <goals>
              <goal>copy-dependencies</goal>
            </goals>
            <configuration>
              <outputDirectory>${data.workdir}</outputDirectory>
              <includeTypes>csv</includeTypes>
              <stripVersion>true</stripVersion>
            </configuration>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
</project>
```


