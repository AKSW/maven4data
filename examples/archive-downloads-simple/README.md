
This example contains a single pom.xml that downloads a file and assigns it a maven artifact id.
By deploying the artifact to one or more of your maven repositories you can later reference it by the artifact id rather than its orginal URL.
This introduces an indirection that allows you migrate a maven repository to a different URL wheras the artifact ids can stay unchanged.

```
mvn process-resources # Downloads the file
mvn install           # Downloads the file and copies it
                      # to the local repository
mvn deploy            # Downloas the file, adds it to the local
                      # repository and deploys it
                      # (according to configuration)
```

