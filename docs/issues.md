---
title: Issues
layout: default
nav_order: 100
---

# Open Issues

The following is a list of short comings that need to be investigated.

* Data artifacts with transitive dependendencies: It is currently unclear (at least to me) whether it is possible to publish maven artifacts that when referenced transitively draw in multiple files (that are outside of JAR files).
Perhaps this could be accomplished with custom life cycles?
* When referencing data with the `build-helper` maven-plugin, the files are copied from the local maven repository to the maven project's workspace.
The copying limits scalability to large datasets - ideally there was an option to create symlinks. It would be possible to fork the plugin but it would be better if this option was added via a PR.


