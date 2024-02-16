---
title: Deploy to WebDAV
layout: default
parent: Deploment
nav_order: 20
---

# Deploy to WebDAV

## Synopsis

This document describes how artifacts can be deployed to a WebDAV service. WebDAV in a protocol that enables write acccess to server content.
It is an extension to HTTP and is supported by many Web servers. Examples include the [Apache HTTP Server](https://httpd.apache.org/), [NGINX](https://www.nginx.com/) and [Nextcloud](https://nextcloud.com/).

## Purpose

* WebDAV is a widely supported protocol. The ability to deploy maven artifacts via this protocol may be useful for archiving purposes.

## Caveats

* ⚠️ Maven's WebDAV provider (`wagon-webdav-jackrabbit`) is deprecated and subject to removal in Maven 4. It is unclear whether and when there will be a replacement.
The example on this page was tested with Maven 3.

* > ⚠️ Just like there is `http://` and its secure version `https://` the same difference exists for WebDAV as it builds upon HTTP(s).
Using `dav://` in cases where secure webdav `davs://` is needed will result in errors.
Typically it will be `permission denied` but it may also be `moved permanently` if the server tries to redirect.

## Approach

* The following `mvn` invocation requires the `pom.xml` and adaptions to the `settings.xml` below.
It will deploy a simple archive to the specified server.
```bash
mvn
  -D"webdav.url=davs://SERVER/nextcloud/remote.php/dav/files/USER" \
  -D"webdav.id.internal=my.webdav.internal" \
  -D"webdav.id.snapshots=my.webdav.snapshots" \
  deploy
```

* Supply user name and password via `~/m2.settings.xml`:
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

* `pom.xml`
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
    <!-- Adjust the URL to your needs -->
    <webdav.base>https://myserver/remote.php/dav/files/Me</webdav.base>
    
    <!-- Adjust the path to your needs -->
    <directory-to-archive>.</directory-to-archive>

    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <wagon-webdav-jackrabbit.version>3.0.0</wagon-webdav-jackrabbit.version>
  <properties>

  <distributionManagement>
    <repository>
      <id>me.myself.internal</id>
      <name>My WebDAV-based Internal Repository</name>
      <url>${webdav.url}</url>
      <uniqueVersion>false</uniqueVersion>
    </repository>
    <snapshotRepository>
      <id>me.myself.snapshots</id>
      <name>My WebDAV-based Snapshot Repository</name>
      <url>${webdav.url}</url>
      <uniqueVersion>false</uniqueVersion>
    </snapshotRepository>
  </distributionManagement>
  
  <repositories>
    <repository>
      <id>me.myself.internal</id>
      <name>My WebDAV-based Internal Repository</name>
      <url>${webdav.url}</url>
    </repository>
    <repository>
      <id>me.myself.snapshots</id>
      <name>My WebDAV-based Snapshot Repository</name>
      <url>${webdav.url}</url>
    </repository>
  </repositories>

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
