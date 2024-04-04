---
title: Maven-RDF Sync
layout: default
nav_order: 60
has_children: true
---

TODO Refactor mvn-rdf-sync into pages for: artifact change events, metadata generation and triple store sync.

# Synchronizing a Triple Store with Maven Repository Data

## Source Code

The source code for `mvn-rdf-sync` is located at: https://github.com/Scaseco/mvn-rdf-sync

## Synopsis

* This chapter presents a lightweight trigger-based approach to realize "build actions" (or "bots") over local maven repositories. A local maven repository is simply a certain directory structure.
  These bots can be used to automatically create new maven projects for producing RDF metadata.

## Purpose

* Metadata artifacts are just plain maven artifacts whose content describes another artifact.
* A large part of RDF metadata generation is agnostic of the content of a dataset and can be fully automated. In those cases, a user should not need to manually set up metadata projects.

## Abstract Approach

The `mvn-rdf-sync` approach comprises two separate processes:

1. A *file system watch* on a (local) maven repository notifies raises events whenever the repository content changes.
2. The event is transmitted to an appropriate receiver.
3. A *filter* discards irrelevant events, such as changes to non-dataset artifacts.
4. If a dataset is deployed (which is not a metadata dataset), then automatically create an instance of a template maven project, and run the build.

TODO architecture chart with the addition of prepublish and triple store loading


### Concrete Approach

1. A simple way to watch a directory recursively for changes is `inotifywait`. This commands even works from within a docker container on a mounted host folder.
2. A relatively straight forward way to transmit events is with Apache Kafka. The advantage of a messaging protocol is that it is possible to send custom events besides the `inotifyway` source.
   This is useful when one wants to trigger recreation of metadata after changing the routine that produced the matdata.


