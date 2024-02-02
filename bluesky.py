from config import Config
import logging, os
from atproto import Client, models
import requests

def bluesky_config_check():
    if Config.BLUESKY_ENABLED == 'True':
        if None in (Config.BLUESKY_APP_USERNAME, Config.BLUESKY_APP_PASSWORD):
            logging.info("Bluesky disabled, credentials missing")
        else:
            blueskyconfig={'enabled': Config.BLUESKY_ENABLED, 'username': Config.BLUESKY_APP_USERNAME, 'password': Config.BLUESKY_APP_PASSWORD}
            logging.info("Bluesky enabled, credentials OK")
    else:
        blueskyconfig={'enabled': Config.BLUESKY_ENABLED}
        logging.info("Bluesky is disabled, set in config")
    return blueskyconfig


def do_bluesky_notification(story):
    bluesky_config = bluesky_config_check()

    logging.debug("Doing a Bluesky notification...")
    client = Client()
    client.login(bluesky_config['username'], bluesky_config['password'])

    embed_headline = story['headline']
    embed_url = story['url']
    embed_summary = story['description']
    embed_image = story['img']

    # image stuff
    response = requests.get(embed_image)
    img_data = response.content
    upload = client.upload_blob(img_data)
    
    text = Config.TWITTER_STATUS_PREFIX + " " + embed_headline
    # AppBskyEmbedExternal is the same as "link card" in the app
    embed_external = models.AppBskyEmbedExternal.Main(
        external=models.AppBskyEmbedExternal.External(
            title=embed_headline,
            description=embed_summary,
            uri=embed_url,
            thumb=upload.blob
        )
    )

    post_with_link_card = client.send_post(text=text, embed=embed_external)
    print(post_with_link_card)

    return
