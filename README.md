xml-to-discord-post
===

Scrapes XML feeds, e.g. BBC News searching for search terms, alerts in Discord, Twitter, or Bluesky. That's it.

Requires MongoDB (Atlas, cloud hosted mongo) to keep track of what's been posted already.

The following vars need to be defined in .env file
```
# MAIN SETUP
REPEAT_DELAY=300 # how often to repeat in seconds
SOURCE_XML="http://feeds.bbci.co.uk/news/rss.xml http://feeds.bbci.co.uk/news/world/rss.xml http://feeds.bbci.co.uk/news/uk/rss.xml http://feeds.bbci.co.uk/news/health/rss.xml http://feeds.bbci.co.uk/news/education/rss.xml http://feeds.bbci.co.uk/news/science_and_environment/rss.xml http://feeds.bbci.co.uk/news/technology/rss.xml http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml" # think that covers most of them
IMGWIDTH=420 # how big the image is in posts
KEYWORDS="space separated keywords to search for"
LOG_LEVEL="INFO" # DEBUG
SEARCHSPECIFIC="True"

# MONGODB (required)
MONGO_DBSTRING="mongodb+srv://....."
MONGO_DB="mongo_db _name"
MONGO_COLLECTION="mongo_db_collection_name"

# DISCORD NOTIFICATIONS (optional)
DISCORD_NOTIFY="True"
DISCORD_CONTENT="Thing to post in webhook content"
DISCORD_USERNAME="webhook_username_here"
DISCORD_WEBHOOK_URL="a_webhook_url_so_you_can_post_to_discord"

# TWITTER/X (optional)
TWITTER_NOTIFY='True'
TWITTER_CONSUMER_KEY="consumer_key"
TWITTER_CONSUMER_SECRET="consumer_secret"
TWITTER_ACCESS_TOKEN="access_token"
TWITTER_ACCESS_TOKEN_SECRET="access_token_secret"
TWITTER_STATUS_PREFIX="Something on the fron of every post"
TWITTER_BEARER_TOKEN="this_is_probably_a_long_token"

# BLUESKY (optional)
BLUESKY_ENABLED="True"
BLUESKY_APP_USERNAME="my_bluesky_name"
BLUESKY_APP_PASSWORD="xyz ..."
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
$ docker run -it --name container-name -v "$PWD/.env:/.env" darrenwatt:xml-to-discord-post:latest
```
To run from docker-compose, in your docker-compose.yml
```
services:
  xml-to-discord-post:
    image: darrenwatt/xml-to-discord-post:latest
    container_name: xml-to-discord-post
    volumes:
     - ${USERDIR}/docker-stuff/xml-to-discord-post/.env:/.env
```
_
Then run with:
```
$ docker-compose -f ~/docker/docker-compose.yml up -d
```

