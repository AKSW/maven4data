---
title: Attaching Artifacts
layout: default
parent: How-Tos
nav_order: 20
---

# Attaching Artifacts

## Synopsis

This document describes how to use the `build-helper-maven-plugin`'s [attach-artifact-mojo](https://www.mojohaus.org/build-helper-maven-plugin/attach-artifact-mojo.html)
in order to attach arbitrary files to the output of a maven build.
Installing or deploying the output will also install or deploy the attached artifacts.

## Purpose

* Keeps dataset files accessible as separate files - i.e. without bundling them up, for example, as a JAR file.
* Deployment of the maven build output to a Build Artifact Repository Manager such as [Archiva](https://archiva.apache.org/) makes those artifacts easily accessible via HTTP(s).


## Example

* The following example is self contained: Save the following snippet as `pom.xml` and run `mvn package`.


```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd" xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <modelVersion>4.0.0</modelVersion>

  <groupId>org.aksw.maven4data.examples</groupId>
  <artifactId>attach-example</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>pom</packaging>
  <name>Attach Artifact Example</name>

  <properties>
    <filepath>pom.xml</filepath>
    <filetype>xml</filetype>
    <classifier>myclassifier</classifier>

    <build-helper-maven-plugin.version>3.5.0</build-helper-maven-plugin.version>
  </properties>

  <build>
    <plugins>
      <!-- Attach the pom.xml file itself (assumes it is named pom.xml) -->
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>build-helper-maven-plugin</artifactId>
        <version>${build-helper-maven-plugin.version}</version>
        <executions>
          <execution>
            <id>attach-artifacts</id>
            <phase>package</phase>
            <goals>
              <goal>attach-artifact</goal>
            </goals>
            <configuration>
              <artifacts>
                <artifact>
                  <file>${filepath}</file>
                  <type>${filetype}</type>
                  <classifier>${classifier}</classifier>
                </artifact>
              </artifacts>
            </configuration>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
</project>
```

