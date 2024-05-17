xml-to-discord-post
===

Scrapes XML feeds, e.g. BBC News searching for search terms, alerts in Discord or to Twitter. That's it.

Uses MongoDB (Atlas, cloud hosted mongo) to keep track of what's been posted already.

The following vars need to be defined in .env file
```
# database connection string for Atlas
db_string = "MONGO-ATLAS-CONNECTION-STRING"

# discord webhook URL
webhook_url = "DISCORD-WEBHOOK-URL"
```
For the rest of the available config values, see config.py


Docker Image
====

Building:
```
docker buildx create --name multiarch_builder --use # if no multiarch env exists already
docker buildx inspect multiarch_builder --bootstrap
docker buildx build --platform linux/amd64,linux/arm64 -t <tag> --push .\
```

To run locally:
```
$ docker run -it --name container-name -v "$PWD/.env:/.env" darrenwatt/news-xml-alert-discord:latest
```
To run from docker-compose, in your docker-compose.yml
```
services:

  news-alert-discord:

    image: darrenwatt/news-xml-alert-discord:latest

    container_name: news-alert-discord

    volumes:

     - ${USERDIR}/docker/news-alert-discord/.env:/.env

```
Then run with:
```
$ docker-compose -f ~/docker/docker-compose.yml up -d
```

