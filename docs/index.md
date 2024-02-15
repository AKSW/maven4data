---
title: Home
layout: home
nav_order: 10
---

## Maven 4 Data

In a nutshell, this documentation is a guide for how to design Maven projects that can **publish data** with an invocation of:

```bash
mvn deploy
```

This guide presents concepts for one-shot data publishing as well as for automated builds.

### Why not ...

* **use a Workflow Engine?**
There are just too many workflow engines out there, and tying builds to one of them significantly limits portability.
Conversely, every workflow engine is expected to be capable of running a shell script and thus invoke a Maven build.

* **use a different build system rather than Maven?**
One of the main reasons for the choice of maven is that its [naming conventions](artifact-naming.md) fit well with Semantic Web concepts.

### Design Philosophy

* 🌐 :globe_with_meridians: Language Agnostic: The data generator / transformer is in Python rather than Java? No problem.
* 🔄 :arrows_counterclockwise: Reproducible Builds: Run `mvn install` repeatedly to repeatedly carry out the data build.
* 💠 :diamond_shape_with_a_dot_inside: Semantic Web Interoperability: Represent [Maven Coordinates](artifact-naming.md) as URNs for use in RDF documents.

### Maven-based Data Management

This repository contains documentation about how to adapt the Maven ecosystem for data generation and publishing.

These guidelines are not only aimed at making it possible to publish data under the [FAIR principles](https://www.go-fair.org/fair-principles/)
(in brief: findability, accessibility, interoperability, and reusability) but also to have **REPRODUCIBLE** builds, which have become conventional in modern software development.

The idea is simple: Maven provides a framework to version, build and deploy (publish) artifacts. Although artifacts are typically JAR files, it is possible to also publish data artifacts.

