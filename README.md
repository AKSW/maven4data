# aksw-data-deployment
A maven pom.xml file with common settings for deploying data artifacts to the AKSW infrastructure.

You can use this pom as a parent for data deployment projects:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd" xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>org.aksw.data.config</groupId>
    <artifactId>aksw-data-deployment</artifactId>
    <version><!-- check version --></version>
    <relativePath></relativePath>
  </parent>
  <packaging>pom</packaging>
  <!-- ... -->
</project>
```

The available versions are listed [here](https://maven.aksw.org/archiva/#artifact/org.aksw.data.config/aksw-data-deployment).

