CWD = $(shell pwd)

SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

# Maven Clean Install Skip ; skip tests, javadoc, scaladoc, etc
MS = mvn -DskipTests -Dmaven.javadoc.skip=true -Dskip
MCCS = $(MS) clean compile
MCIS = $(MS) clean install

# We need to declare the substitution variables to avoid clases with maven properties
# Maybe we should use a different pattern such as '$[VAR]' (brackets) for envsubst
#ENVSUBST = envsubst '$$groupId $$artifactId $$version $$type $$url $$file $$name $$prefix $$parent $$modules $$artifactItems'
ENVSUBST = envsubst '$$groupId $$artifactId $$version $$type $$name $$prefix $$parent $$modules $$artifactItems'

# Source: https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile
.ONESHELL:
.PHONY: help
.SILENT:
help:  ## Show these help instructions
	@sed -rn 's/^([a-zA-Z_-]+):.*?## (.*)$$/"\1" "\2"/p' < $(MAKEFILE_LIST) | xargs printf "make %-35s# %s\n"

target:
	mkdir -p target

# https://www.mojohaus.org/build-helper-maven-plugin/parse-version-mojo.html

#
# Goals for version manipulation.
#

version-increment-to-snapshot: ## Increment version and add SNAPSHOT qualifier
	mvn build-helper:parse-version versions:set -D"newVersion=\$${parsedVersion.majorVersion}.\$${parsedVersion.minorVersion}.\$${parsedVersion.nextIncrementalVersion}-SNAPSHOT"

#version-increment-to-release: ## Increment version and omit SNAPSHOT qualifier
#	mvn build-helper:parse-version versions:set -D"newVersion=\$${parsedVersion.majorVersion}.\$${parsedVersion.minorVersion}.\$${parsedVersion.nextIncrementalVersion}"

#version-increment-with-qualifier: ## Increment version and retain qualifier if present
#	mvn build-helper:parse-version versions:set -D"newVersion=\$${parsedVersion.majorVersion}.\$${parsedVersion.minorVersion}.\$${parsedVersion.nextIncrementalVersion}\$${parsedVersion.qualifier?}"

version-qualifier-snapshot: ## Append SNAPSHOT if not already present
	mvn build-helper:parse-version versions:set -D"newVersion=\$${parsedVersion.majorVersion}.\$${parsedVersion.minorVersion}.\$${parsedVersion.incrementalVersion}-SNAPSHOT"

version-qualifier-remove: ## Remove any present version qualifier
	mvn build-helper:parse-version versions:set -D"newVersion=\$${parsedVersion.majorVersion}.\$${parsedVersion.minorVersion}.\$${parsedVersion.incrementalVersion}"

version-commit: ## Commit the version
	mvn versions:commit

version-rollback: ## Rollback uncommitted version changes
	mvn versions:revert

.SILENT:
version-latest: ## Set to the latest released version and increment if exists it otherwise leave as is
	# if VER="$$($(MAKE) -f $(lastword $(MAKEFILE_LIST)) print-released-version)"; then
	VER=$$(mvn -U build-helper:released-version help:evaluate -q -DforceStdout -D"expression=releasedVersion.version")
	if [[ "$$VER" == *"null"* ]]; then
	  echo "No latest version found."
	else
	  mvn versions:set -D"newVersion=$$VER"	  
	fi
	# && mvn versions:set -D"newVersion=$v"

.SILENT:
print-released-version: ## Print out the latest released version or fail with non-zero exit code
	VER=$$(mvn -U build-helper:released-version help:evaluate -q -DforceStdout -D"expression=releasedVersion.version")
	[[ "$$VER" == *"null"* ]] && exit 1 || echo "$$VER"

list-versions: ## Print all versions
	DEST="target/sha"
	mkdir -p "$$DEST"
	mvn -U dependency:copy -D'artifact=$${project.groupId}:$${project.artifactId}:$${project.version}:$${output.filetype}.sha1' -D"outputDirectory=$$DEST"
	FILE=$$(find "$$DEST/"*)
	REMOTE_HASH="$$(cat "$$FILE")"
	#http://maven.aksw.org/repository/internal/org/coypu/data/disasters/disasters/maven-metadata.xml

version-increment-on-change: | target ## Retrieve the hash of the latest release
	LOCAL_HASH=$$(sha1sum target/disasters.nt.bz2 | cut -f 1 -d ' ')
	DEST="target/sha"
	mkdir -p "$$DEST"
	mvn -U dependency:copy -D'artifact=$${project.groupId}:$${project.artifactId}:$${project.version}:$${output.filetype}.sha1' -D"outputDirectory=$$DEST"
	FILE=$$(find "$$DEST/"*)
	REMOTE_HASH="$$(cat "$$FILE")"
	echo "$$LOCAL_HASH"
	echo "$$REMOTE_HASH"
	if [[ "$$LOCAL_HASH" == "$$REMOTE_HASH" ]]; then
	  echo "Local and remote hashes are equal - nothing to be done"
	else
	  ## 
	  $(MAKE) version-latest # TODO We need a make release version goal
	  mvn -D"generate-data=false" deploy
	  $(MAKE) version-increment-to-snapshot
	fi



