#!/bin/bash
set -euo pipefail

echoerr() { echo "$@" 1>&2; }

USAGE="Usage: $(basename "$0") command

This script compares the checksum of a local pom.xml's output file with the checksum
of the latest (remote) release version.
If the checksums differ then the provided command is evaluated.

Things to consider:
- The local pom MUST be a SNAPSHOT otherwise it will be detected as the latest release!
- Beware that relases are cached in the local repository and information may be read from there.
- The pom must have the properties 'output.path' and 'output.filetype' defined.
- Retrieval of the checksum currently creates a warning:
  'org.eclipse.aether.transfer.ChecksumFailureException: Checksum validation failed, no checksums available'
  The reason is that we treat the checksum as an artifact so maven tries to validate its checksum.
  If you know a better way for checksum retrieval let me know :)

Example:
- Deploy on change - If the local snapshot differs from the latest release then
  remove snapshot, deploy and commit the version without snapshot:
  ./on-change.sh 'mvn versions:set -DremoveSnapshot; mvn deploy -DskipGenerateData; mvn versions:commit'

Changelog:
- 2023-12-14 Claus Stadler - First working version
"

if [ $# -ne 1 ]
then
    echo "$USAGE"
    exit 1;
fi;

CMD="$1"

IS_CHANGE=0

LOCAL_FILE=`mvn help:evaluate -q -DforceStdout -D'expression=output.path'`
if [ ! -f "$LOCAL_FILE" ]; then
  echo "File $LOCAL_FILE does not exist"
  exit 1
fi

echoerr "Retrieving latest remote version ..."
REMOTE_LATEST_VERSION=`mvn -U build-helper:released-version help:evaluate -q -DforceStdout -D"expression=releasedVersion.version"`
if [[ "$REMOTE_LATEST_VERSION" == *"null"* ]]; then
  echoerr "Note: No latest remote version found."
  IS_CHANGE=1
else
  echoerr "Detected latest remote version: $REMOTE_LATEST_VERSION"
fi

if [ $IS_CHANGE -eq 0 ]; then
  echoerr "Retrieving remote hash..."
  TMPDIR="$(mktemp -d)"
  trap 'rm -rf -- "$TMPDIR"' EXIT
  mvn -U dependency:copy -D'artifact=${project.groupId}:${project.artifactId}:'"$REMOTE_LATEST_VERSION"':${output.filetype}.sha1' -D"outputDirectory=$TMPDIR"
  FILE=`find "$TMPDIR/"*`
  REMOTE_HASH=`cat "$FILE"`

  LOCAL_HASH=`sha1sum "$LOCAL_FILE" | cut -f 1 -d ' '`
  echoerr "Local: $LOCAL_HASH"
  echoerr "Remote: $REMOTE_HASH"

  # Either the hashes are equal or there is a change
  [ "$LOCAL_HASH" = "$REMOTE_HASH" ] || IS_CHANGE=1
fi

if [ $IS_CHANGE -eq 1 ]; then
  echoerr "Change detected, running provided command"
  eval "$CMD"
fi


