---
title: Deploy to WebDAV
layout: default
parent: Deployment
nav_order: 20
---

# Deploy to WebDAV

## Synopsis

This document describes how artifacts can be deployed to a WebDAV service. WebDAV in a protocol that enables write acccess to server content.
It is an extension to HTTP and is supported by many Web servers. Examples include the [Apache HTTP Server](https://httpd.apache.org/), [NGINX](https://www.nginx.com/) and [Nextcloud](https://nextcloud.com/).

## Purpose

* WebDAV is a widely supported protocol. The ability to deploy maven artifacts via this protocol may be useful for archiving purposes.

## Caveats

> ⚠️ Maven's WebDAV provider (`wagon-webdav-jackrabbit`) is deprecated and subject to removal in Maven 4. It is unclear whether and when there will be a replacement.
The example on this page was tested with Maven 3.

> ⚠️ Just like there is `http://` and its secure version `https://` the same difference exists for WebDAV as it builds upon HTTP(s).
Using `dav://` in cases where secure webdav `davs://` is needed will result in errors.
Typically it will be `permission denied` but it may also be `moved permanently` if the server tries to redirect.

## Approach

The following `mvn` invocation requires appropriately adapted versions of the `pom.xml` and `settings.xml` files as described below.
It will deploy a simple archive to the specified server using:

```bash
mvn -P webdav deploy
```

> ℹ️ It is generally good practice to put distribution configurations, such as that for the webdav deployment - into profiles.
This allows one to easiliy deploy to a specific destination.

Supply user name and password with appropriate `<server>` sections in the `~/m2/settings.xml`:
```xml
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">

  <servers>
    <server>
      <id>my.webdav.internal</id>
      <username>USERNAME</username>
      <password>PASSWORD</password>
    </server>
    <server>
      <id>et.webdav.snapshots</id>
      <username>USERNAME</username>
      <password>PASSWORD</password>
    </server>
  </servers>
</settings>
```

The `pom.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.aksw.maven4data.examples</groupId>
  <artifactId>my-archived-directory-with-webdav</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  
  <properties>
    <!-- Adjust the following settings your needs -->
    <webdav.url>davs://SERVER/nextcloud/remote.php/dav/files/USERNAME</webdav.url>
    
    <!-- The values for these properties must match with the server ids in settings.xml -->
    <webdav.id.internal>my.webdav.internal</webdav.id.internal>
    <webdav.id.snapshots>my.webdav.snapshots</webdav.id.snapshots>
    
    <!-- Adjust the path to your needs -->
    <directory-to-archive>.</directory-to-archive>

    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <wagon-webdav-jackrabbit.version>3.0.0</wagon-webdav-jackrabbit.version>
  </properties>
  
  <repositories>
    <repository>
      <id>${webdav.id.internal}</id>
      <name>My WebDAV-based Internal Repository</name>
      <url>${webdav.url}</url>
    </repository>
    <repository>
      <id>${webdav.id.snapshots}</id>
      <name>My WebDAV-based Snapshot Repository</name>
      <url>${webdav.url}</url>
    </repository>
  </repositories>

  <profiles>
    <profile>
      <id>webdav</id>
      <distributionManagement>
        <repository>
          <id>${webdav.id.internal}</id>
          <name>My WebDAV-based Internal Repository</name>
          <url>${webdav.url}</url>
          <uniqueVersion>false</uniqueVersion>
        </repository>
        <snapshotRepository>
          <id>${webdav.id.snapshots}</id>
          <name>My WebDAV-based Snapshot Repository</name>
          <url>${webdav.url}</url>
          <uniqueVersion>false</uniqueVersion>
        </snapshotRepository>
      </distributionManagement>      
    </profile>
  </profiles>

  <build>
    <extensions>
      <extension>
        <groupId>org.apache.maven.wagon</groupId>
        <artifactId>wagon-webdav-jackrabbit</artifactId>
        <version>${wagon-webdav-jackrabbit.version}</version>
      </extension>
    </extensions>
  
    <resources>
      <resource>
        <directory>${directory-to-archive}</directory>
      </resource>
    </resources>
  </build>
</project>
```
