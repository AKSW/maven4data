---
title: Messaging
layout: home
parent: Maven-RDF Sync
nav_order: 20
---

# Messaging

## Synopsis

Once changes to a maven repository [are detected](change-detection.md), appropriate messages need to be sent out and relevant components need to be notified.

## Purpose

A message queuing system helps to decouple message producers from receivers.
Furthermore, event sources can be abstracted, for example, a message requesting triggering re-processing of metadata generation may originate from a
repository-change-detector or from a manual request by the user.
Message queueing systems may feature fault tolerance, such as prevention of data loss in case of server crashes.

## REST API vs Message Queuing

A main difference between sending a message vs calling e.g. a REST method is, that the former allows for event listeners to be (un)registered dynamically.
Then of course the fault tolerance.
One may create a REST method whose implementation sends out messages via a message queuing system.

## Approach

mvn-rdf-sync uses Apache Kafka for messaging.
Apache Kafka is popular, easy to use, and also works from the command line.
For now we just point to the [Quick Start Guide](https://kafka.apache.org/quickstart).

