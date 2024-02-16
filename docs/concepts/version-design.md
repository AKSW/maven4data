---
title: Version Design
layout: default
parent: Concepts
nav_order: 30
---

## Version Design Considerations

* Semantic Versioning: A semantic version string is made up from 3 integers in the format `major.minor.incremental`.

An increment in only the ...
  * ... `incremental` component signifies a non-breaking bug fix.
  * ... `minor` component signifies a non-breaking feature addition.
  * ... `major` component signifies a breaking change.

Translating these to datasets would roughly mean:

* An incremental update would be fixing labels
* A minor update would be the addition of new instances and properties
* A major update would be schema changes or the removal of instances or properties (as those instances may have been referenced in the downstream process)

* It may be tempting to use the format `yyyy.MM.dd` such as `<version>2024.02.15</version>`, however this may make it difficult to publish updated versions of data at that time later on. For example,
if it turns out there was a bug in the data generator and several versions are broken.


Possible mitigations:
* Make the data generator revision part of the groupId such as `<groupId>org.myorg.myproject.datagen.v2</groupId>`
* Reserve the major version field for revisions `<version>1.20240215.0</version>`

