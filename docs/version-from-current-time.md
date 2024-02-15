---
title: Version from current Time
layout: default
nav_order: 30
---

# Version from current Time

## Synopsis

## Caveats

* The [build-helper:parse-version](https://www.mojohaus.org/build-helper-maven-plugin/parse-version-mojo.html) goal can only parse versions whose components are in the 32bit integer range.
A minute-granularity timestamp of format `yyyyMMddHHmm` exceeds that range.

## Approach

* Update the version of the pom.xml itself with
```bash
mvn -P increment-version validate
```
Note, this will create a backup copy of the `pom.xml` named `pom.xml.versionsBackup`.
* Use `mvn versions:rollback` to revert the change; effectively replacing the `pom.xml` with the backup copy.
* Use `mvn versions:commit` to remove the backup copy.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.aksw.maven4data.examples</groupId>
  <artifactId>version-from-current-time</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <packaging>pom</packaging>

  <name>Version from current Time</name>
  <description>Self-update the version of this pom with "mvn -P increment-version validate"</description>

  <properties>
    <build-helper-maven-plugin.version>3.5.0</build-helper-maven-plugin.version>
    <versions-maven-plugin.version>2.16.2</versions-maven-plugin.version>
  </properties>

  <profiles>
    <!-- Activating this profile sets the version of this pom.xml to the current timestamp (minute granularity) -->
    <profile>
      <id>increment-version</id>
      <build>
        <plugins>
        
          <!-- This plugin execution sets the property "versionTimestamp" -->
          <!-- to a value based on the current date -->
          <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>build-helper-maven-plugin</artifactId>
            <version>${build-helper-maven-plugin.version}</version>
            <executions>
              <execution>
                <id>version-timestamp-property</id>
                <goals>
                  <goal>timestamp-property</goal>
                </goals>
                <configuration>
                  <!-- format the timestamp such that the components fit into integers -->
                  <name>versionTimestamp</name>
                  <pattern>yyyyMMdd.HHmm</pattern>
                  <locale>en_US</locale>
                  <timeZone>UTC</timeZone>
                </configuration>
              </execution>
              <execution>
                <id>parse-version</id>
                <goals>
                  <goal>parse-version</goal>
                </goals>
              </execution>
            </executions>
          </plugin>

          <!-- This plugin execution updates this pom's version -->
          <!-- using the computed "versionTimestamp" property -->
          <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>versions-maven-plugin</artifactId>
            <version>${versions-maven-plugin.version}</version>
            <executions>
              <execution>
                <phase>validate</phase>
                <goals>
                  <goal>set</goal>
                </goals>
                <configuration>
                  <!-- build helper can only parse integers. A timestamp of minute granularity such as -->
                  <!-- yyyyMMddHHmm is literally too *long* (pun intended) -->
                  <newVersion>${parsedVersion.majorVersion}.${versionTimestamp}-SNAPSHOT</newVersion>                  
                </configuration>
              </execution>
            </executions>
          </plugin>
        </plugins>
      </build>
    </profile>
  </profiles>
</project>
```

