---
layout: default
title: Overview
nav_order: 10
---

# Maven 4 Data

## Synopsis

This documentation is a guide for how to design Maven projects that can **generate** and **publish** data with an mere invocation of:

```bash
mvn deploy
```

This guide presents concepts for one-shot data publishing as well as for automated builds.

## Why not ...

* **use a Workflow Engine?**
There exist many workflow engines, and tying builds to one of them significantly limits portability.
Conversely, every workflow engine is expected to be capable of running a shell script and thus invoke a Maven build.

* **use a different build system rather than Maven?**
One of the main reasons for the choice of maven is that its [naming conventions](artifact-naming.md) fit well with Semantic Web concepts.

## Design Philosophy

* 🌐 Programming Language Agnostic: The data generation code is in Python rather than Java? No problem.
* 🔄 Reproducible Builds: Run `mvn install` repeatedly to repeatedly carry out the data build.
* 💠 Semantic Web Interoperability: Represent [Maven Coordinates](artifact-naming.md) as URNs for use in RDF documents.
* 🌈 Data Format Agnostic: Although this guide has a Semantic Web / RDF bias, many concepts can be applied to any data format, such as CSV, XML, JSON, text, PDF or ZIP archives.

## Maven-based Data Management

This repository contains guidelines about how to adopt, and adapt and maybe sometimes bend the Maven ecosystem for data generation and publishing.

These guidelines are not only aimed at making it possible to publish data under the [FAIR principles](https://www.go-fair.org/fair-principles/)
(in brief: findability, accessibility, interoperability, and reusability) but also to have **REPRODUCIBLE** builds, which have become conventional in modern software development.

The idea is simple: Maven provides a framework to version, build and deploy artifacts. Although artifacts are typically JAR files, it is possible to also publish data artifacts.

