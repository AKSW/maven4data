---
title: Maven Repository Events
layout: default
parent: Maven-RDF Sync
nav_order: 20
---


# Maven Repository Change Detection

## Synopsis

This page lists approaches about how to detect changes to artifacts in a Maven repository.

## Purpose

The ability to detect changes to a Maven repository allows one to automate several processes:

* Meta-data generation: Automatically generate VoID, DCAT and PROV-O models from uploaded datasets.
* RDF-Store synchronization: Automatically update an RDF store with information about the Maven repository. Effectively enables querying Maven repositories with Data.

## Approaches

### inotifywait

`inotifywait` is a command line tool capable of watching directories recursively for changes.
It works well on linux distributions - even when invoked within docker containers on a folder mounted from the host.

The following line will report any closing of a file (after write) or deletion in the repository in the format `EVENTS PATH/FILENAME`:
```
inotifywait "$HOME/.m2/repository" --recursive --monitor --format '%e %w%f' --event CLOSE_WRITE --event DELETE
```

Example output:
```
CLOSE_WRITE,CLOSE /home/user/.m2/repository/org/example/myproject/myartifact/1.0.0-SNAPSHOT/myartifact-1.0.0-SNAPSHOT.jar
```

### Repository Manager Hooks and Plugins

Repository Managers may either directly support hooks or they may allow for third party plugins that could supply this functionality.

* Archiva?
* Artifactory?

Contributions to this section are welcome.

### Polling

For completeness, the following script sketches for how one could detect changes to a directory using polling.
The polling could be triggered periodically by a CRON job.

```
# Ensure before.txt exists
touch before.txt

# Generate a recursive directory listing
find "$MVN_REPO" | LC_ALL=C sort -u > current.txt

# Compute a diff
diff current.txt before.txt

# Process the diff

# Move current state to prior state
mv current.txt before.txt
```



