

In your `$HOME/.m2/settings.xml`:
```
<server>
        <id>dm.coypu.org</id>
        <username>CKAN_USER_NAME</username>
        <password>CKAN_API_KEY</password>
</server>


```

```bash
mvn -D maven.deploy.skip deploy
```

