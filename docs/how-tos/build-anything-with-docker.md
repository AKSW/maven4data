---
title: Build Anything with Docker
layout: default
parent: How-Tos
nav_order: 50
---

## Build Anything with Docker

The powerful and well-documented [io.fabric8:maven-docker-plugin](https://dmp.fabric8.io/) can be used to build docker images and run docker containers as part of maven builds. 

In order to package data generation as a self-contained maven build, the two major steps are:

1. Publish a code-artifact with the scripts and resources that need to run in the container.
2. Set up a the data generator `pom.xml` that makes the code-artifact available for the build with the docker-maven-plugin.

### Example

The setup at [examples/disasters-rdfizer](https://github.com/AKSW/aksw-data-deployment/tree/develop/examples/disasters-rdfizer) contains the 2 folders:

1. `code`: This folder contains the actual data generation script and a `pom.xml` file in order to package and version it.
2. `generator`: This is a `pom.xml` file that builds and runs a docker container from the `code`.

#### Code

The following excerpt of the `pom.xml` for archiving anything in a `src` folder is shown below:

```xml
<!-- <project> -->

  <groupId>org.coypu.disasters.code</groupId>
  <artifactId>disasters-downloader</artifactId>
  <version>0.0.2</version>

  <!-- Inherit settings from this parent -->
  <parent>
    <groupId>org.aksw.data.config</groupId>
    <artifactId>aksw-data-deployment</artifactId>
    <version>0.0.8</version>
    <relativePath></relativePath>
  </parent>

  <!-- JAR files are ZIP files, so we are actually just creating a ZIP file here -->
  <packaging>jar</packaging>

  <!-- Include the src folder as a resource. Its contents will be added to the root of the JAR bundle. -->
  <build>
    <resources>
      <resource>
        <directory>src</directory>
      </resource>
    </resources>
  </build>
  
<!-- </project> -->
```

#### Generator

The steps to set up the data generator as a `pom.xml` is as follows:


1. Use the `maven-dependency-plugin` to unpack the code bundle into a `temp-resources` folder. To make the folder name configurable, we introduce a property for it.
```xml
    <!-- Relative folder where to unpack the code bundle -->
    <localUnpackRelDir>temp-resources</localUnpackRelDir>

```

Actually we would like to place those files into the `target` folder, however the `docker-maven-plugin` does not appear to support making files in that folder part of the docker build.

2. In order for `mvn clean` to delete the temporary files, we add the `maven-clean-plugin`
```xml
      <!-- Clear the local temp directory on clean -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-clean-plugin</artifactId>
        <configuration>
          <filesets>
            <fileset>
              <directory>${localUnpackRelDir}</directory>
            </fileset>
          </filesets>
        </configuration>
      </plugin>
```
  
3. We need to declare which files to attach to the build output.

4. Configure the docker maven plugin

The relevant parts are: In the `assemblies` section, the `descriptorRef` needs to be set to `project` in order to include everything in the current folder - especially the `temp-resources` folder.
The `targeDir` is the path in the container where to place the files from the host.
```xml
<assemblies>
  <assembly>
    <name>deps-release</name>
    <descriptorRef>project</descriptorRef>
    <targetDir>${containerBaseAbsDir}</targetDir>
  </assembly>
</assemblies>
```

Set up the commands that need to be run during build. For example, install `lbzip2` and run `pip install`. In this case, the file `requirements.txt` originates from the code bundle.
```xml
<runCmds>
  <run>apt-get update &amp;&amp; DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --assume-yes lbzip2</run>
  <run>python -m venv venv &amp;&amp; . venv/bin/activate &amp;&amp; pip install -r requirements.txt</run>
</runCmds>
```
<sub>TODO Test if CDATA blocks removes the need for &amp;amp;</sub>



Tell maven to build the docker image, start the container, copy out the generated files and stop the container when done during the `process-resources` phase. 

```xml
<execution>
  <id>run-container</id>
  <phase>process-resources</phase>
  <goals>
    <goal>build</goal>
    <goal>start</goal>
    <goal>copy</goal>
    <goal>stop</goal>
  </goals>
</execution>
```
