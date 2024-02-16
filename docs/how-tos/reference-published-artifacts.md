---
title: Referencing Non-JAR Artifacts
layout: default
parent: How-Tos
nav_order: 30
---

# Referencing Artifacts

## Downloading an artifact with the CLI

Attached artifacts can be referenced using the `pom.xml`'s [GAV](maven-concepts.md) plus the attached type and classifier.
For example, the `pom.xml` below will install itself as `org.aksw.maven4data.examples:attach-example:1.0.0-SNAPSHOT:xml:example`:

```bash
mvn dependency:copy -D'artifact=org.aksw.maven4data.examples:attach-example:1.0.0-SNAPSHOT:xml:myclassifier' \
  -Dmdep.stripVersion=true -D'outputDirectory=.'
```
This will create the file `attach-example-myclassifier.xml` in the local directory. The filename follows the pattern `[artifactId]-[classifier].[type]`.

## Downloading an artifact from the pom.xml

```bash
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.aksw.maven4data.examples</groupId>
  <artifactId>download-maven-artifact</artifactId>
  <version>1.0.0-SNAPSHOT</version>

  <packaging>pom</packaging>

  <properties>
    <datasetDirectory>${project.build.directory}/datasets</datasetDirectory>
  </properties>

  <build>
    <resources>
      <resource>
        <directory>${project.build.directory}/datasets</directory>
      </resource>
    </resources>

    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-dependency-plugin</artifactId>
        <executions>
          <execution>
            <id>resource-dependencies</id>
            <phase>process-resources</phase>
            <goals>
              <goal>copy</goal>
            </goals>
            <configuration>
              <stripVersion>true</stripVersion>
              <artifactItems>

                <artifactItem>
                  <groupId>org.aksw.maven4data.examples</groupId>
                  <artifactId>climatetrace-fluorinated-gases</artifactId>
                  <version>0.2.0</version>
                  <type>zip</type>
                  <overWrite>true</overWrite>
                  <outputDirectory>${datasetDirectory}</outputDirectory>
                </artifactItem>

              </artifactItems>
            </configuration>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
</project>
```
