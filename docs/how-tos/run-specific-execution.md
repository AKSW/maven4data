---
title: Run a specific plugin execution
layout: default
parent: How-Tos
nav_order: 50
---

# Run a specific plugin execution

## Synopsis

This document shows how to run a specific execution of a plugin goal defined in a POM.

## Purpose

When plugins are defined in a POM such as in the snippet below, it is often useful to be able to run a specific execution declared in a POM from the command line.

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-compiler-plugin</artifactId>
  <version>...</version>
  <configuration>
    <release>17</release>
  </configuration>
  <!-- The execution below is implicit and can be omitted for the compiler plugin -->
  <executions>
    <execution>
      <id>default-compile</id>
      <goal>compile</goal>
      <phase>compile</goal>
    </execution>
  </executions>
</plugin>
```

## Approach

In general, the syntax to run a specific execution in a POM is:

```bash
mvn pluginName:goal@executionId
```

For example, in a typical Java project this line would run compilation only:

```bash
mvn compiler:compile@default-compile
```

Maven resolves `compiler` to `maven-compiler-plugin`.


For plugins with the name pattern `dataproducer-maven-plugin` it should also work to only use `dataproducer:goal@executionId`.

