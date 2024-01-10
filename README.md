news-alert-discord
===

Scrapes BBC News homepage searching for search terms, alerts in Discord or to Twitter. That's it.

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

https://cloud.docker.com/repository/docker/darrenwatt/news-alert-discord

To run locally:
```
$ docker run -it --name news-alert-discord -v "$PWD/.env:/.env" darrenwatt/news-alert-discord:latest
```
To run from docker-compose, in your docker-compose.yml
```
services:

  news-alert-discord:

    image: darrenwatt/news-alert-discord:latest

    container_name: news-alert-discord

    volumes:

     - ${USERDIR}/docker/news-alert-discord/.env:/.env

```
Then run with:
```
$ docker-compose -f ~/docker/docker-compose.yml up -d
```

