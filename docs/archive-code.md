## Archiving Resources (Scripts and Non-Java Code)

Maven can be used bundle any folder up as a JAR archive by declaring that folder as a resource.

For example, assume your project has the following structure:

```
|- README.md
|- src
|  |- requirements.txt
|  |- run.sh
|  |- LICENSE.txt
|
|- LICENSE.txt # symlink to /src/LICENSE.txt
```

The following `pom.xml` can be used to package the content of the `src` folder up as a versioned JAR file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>org.aksw.myproject.mydataset.code</groupId>
	<artifactId>data-generation-script</artifactId>
	<version>0.0.2</version>

  <!-- Inherit settings from this parent -->
	<parent>
		<groupId>org.aksw.data.config</groupId>
		<artifactId>aksw-data-deployment</artifactId>
		<version>0.0.8</version>
		<relativePath></relativePath>
	</parent>

  <!-- JAR files are ZIP files, so we are actually just creating a ZIP file here -->
	<packaging>jar</packaging>

  <!-- Include the src folder as a resource. Its contents will be added to the root of the JAR bundle. -->
	<build>
		<resources>
			<resource>
				<directory>src</directory>
			</resource>
		</resources>
	</build>
</project>
```
