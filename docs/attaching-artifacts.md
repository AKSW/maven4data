---
title: Attaching Artifacts
layout: default
nav_order: 30
---

## Attaching Artifacts

### Summary

This document describes how to use the `build-helper-maven-plugin`'s [attach-artifact-mojo](https://www.mojohaus.org/build-helper-maven-plugin/attach-artifact-mojo.html)
in order to attach arbitrary files to the output of a maven build.
Installing or deploying the output will also install or deploy the attached artifacts.

## Purpose

* Keeps dataset files accessible as separate files - i.e. without bundling them up, for example, as a JAR file.
* Deployment of the maven build output to a Build Artifact Repository Manager such as [Archiva](https://archiva.apache.org/) makes those artifacts easily accessible via HTTP(s).

## Referencing attached Artifacts

Attached artifacts can be referenced using the `pom.xml`'s [GAV](maven-concepts.md) plus the attached type and classifier.
For example, the `pom.xml` below will install itself as `org.aksw.maven4data.examples:attach-example:1.0.0-SNAPSHOT:xml:example`:

```bash
mvn dependency:copy -D'artifact=org.aksw.maven4data.examples:attach-example:1.0.0-SNAPSHOT:xml:myclassifier' \
  -Dmdep.stripVersion=true -D'outputDirectory=.'
```
This will create the file `attach-example-myclassifier.xml` in the local directory. The filename follows the pattern `[artifactId]-[classifier].[type]`.


## Example

* The following example is self contained: Save the following snippet as `pom.xml` and run `mvn install`.


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

