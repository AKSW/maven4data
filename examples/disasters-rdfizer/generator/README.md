Experimental Maven wrapper for the disaster RDFizer by Implisense.


### Data Generation
This project uses maven's default lifeycle [https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html#default-lifecycle].
The setup of this project binds data generation to the `process-resources` phase.

Due to the nature of maven's life cyle, the order of phases is `process-resources`, `install`, `deploy` - whereas the a latter phase runs all former ones.
In other words, if `process-resources` was already invoked, then running `deploy` will run it again.

For this reason, the project provides a `generate-data=false` property for disabling data generation. 

```
mvn process-resources
```

To install or deploy the data without running the generation again you can use the following commands:
```
mvn -Dgenerate-data=false install
mvn -Dgenerate-data=false deploy
```


### Notes
A proper documentation should be set up at https://github.com/AKSW/aksw-data-deployment

* Typical invocation with `mvn -P increment-version clean process-resources`
* Use `mvn -Ddocker.skip.build` to skip the image build. With a `does-docker-image-exist-maven-plugin` we could auto-derive the value; maybe the docker plugin can already query the docker daemon for whether an image with a given tag already exists and set a property?
* skipGenerateData should be renamed to something like datagen.skip or data.generate.skip


### Issues
- [ ] Maven Deploy rebuilds the dataset - needs fiddling with phases or in the worst case profiles
- [ ] The python script itself should be backed up as a versioned artifact, which is retrieved and added to the image dynamically - or rather: The whole docker image (with all dependencies to make it self contained).
      A variant could be to include the whole script in the pom.xml file (CDATA) to make it self-contained. Or: We create a jar bundle from it - but then every dataset generation would include a jar with the script - needs more thought.

