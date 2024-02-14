---
nav_order: 30
---

## Download and Archive a URL

A `pom.xml` setup to download a single URL and archive it under an artifact ID is shown below.
In this pom design, the property `input.url` points to the original URL source. The property can be read out by scripts such as CI processes to auto-generate information.

The approach is:

1. Use the `wget` goal of the `download-maven-plugin` to download the URL to a local file.
2. Attach the artifact to the build with the `build-helper-maven-plugin`.


```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd" xmlns="http://maven.apache.org/POM/4.0.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>org.aksw.data.config</groupId>
    <artifactId>aksw-data-deployment</artifactId>
    <version>0.0.8</version>
    <relativePath></relativePath>
  </parent>

  <groupId>org.coypu.data.climatetrace</groupId>
  <artifactId>climatetrace-agriculture</artifactId>
  <version>0.2.0</version>
  <packaging>pom</packaging>
  <name>Climate TRACE - Agriculture</name>
  <description>Climate TRACE archive for the sector "Agriculture".</description>
  <url>https://climatetrace.org</url>

  <licenses>  
    <license>
      <name>Creative Commons Attribution 4.0</name>
      <url>https://creativecommons.org/licenses/by/4.0/</url>
    </license>
  </licenses>

  <properties>
    <!-- Machine readable original download link (may eventually break) -->
    <input.url>https://downloads.climatetrace.org/v02/sector_packages/agriculture.zip</input.url>
    <output.filename>agriculture.zip</output.filename>
    <output.filetype>zip</output.filetype>
  </properties>

  <build>
    <plugins>    
      <!-- Download of a URL to file -->
      <plugin>
        <groupId>com.googlecode.maven-download-plugin</groupId>
        <artifactId>download-maven-plugin</artifactId>
        <executions>
          <execution>
            <id>download-dataset</id>
            <phase>process-resources</phase>
            <goals>
              <goal>wget</goal>
            </goals>
          </execution>
        </executions>
        <configuration>
          <url>${input.url}</url>
          <unpack>false</unpack>
          <outputDirectory>${project.build.directory}</outputDirectory>
          <outputFileName>${output.filename}</outputFileName>
          <skipCache>true</skipCache>
        </configuration>
      </plugin>

      <!-- Deployment of downloaded file -->
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>build-helper-maven-plugin</artifactId>
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
                  <file>${project.build.directory}/${output.filename}</file>
		  <type>${output.filetype}</type>
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

