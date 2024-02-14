#!/bin/bash
set -euo pipefail

mvn clean -Pincrement-version process-resources

# Deploy (without local install)
./on-change.sh 'mvn versions:set -DremoveSnapshot; mvn deploy -Dmaven.install.skip -DskipGenerateData; mvn versions:commit'

# Install locally
#./on-change.sh 'mvn versions:set -DremoveSnapshot; mvn install -DskipGenerateData; mvn versions:commit'

