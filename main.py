from ast import keyword
from config import Config
from pymongo import MongoClient
import xml.dom.minidom
import requests, time, json, re, tweepy, logging


Config = Config()
logging.basicConfig(format=Config.LOG_FORMAT, level=Config.LOG_LEVEL)
logging.info("Yoyoyo, starting up in the house!")


mongoclient = MongoClient(Config.MONGO_DBSTRING)
db = mongoclient[Config.MONGO_DB]
collection = db[Config.MONGO_COLLECTION]


if Config.TWITTER_NOTIFY == 'True':
    logging.info("Tweeting is enabled")

    twitter_consumer_key = Config.TWITTER_CONSUMER_KEY
    twitter_consumer_secret = Config.TWITTER_CONSUMER_SECRET
    twitter_access_token = Config.TWITTER_ACCESS_TOKEN
    twitter_access_token_secret = Config.TWITTER_ACCESS_TOKEN_SECRET

    client = tweepy.Client(
    consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret,
    access_token=twitter_access_token, access_token_secret=twitter_access_token_secret
    )

else:
    logging.info("Tweeting is disabled")


# keyword handling

keywords=Config.KEYWORDS.split()

if Config.SEARCHSPECIFIC == 'True':
    # match exact terms only
    reg = re.compile(r'(?i)\b(?:%s)\b' % '|'.join(keywords))
else:
    # match any partial term, this seems to work, I suck at regex so this might well be wrong
    reg = re.compile(r'(?i)%s' % '|'.join(keywords))

logging.info("regex output: %s", reg)

## end of keyword handling


def scrape_bbc_news_xml(url):
    logging.info("getting stories ...")
    logging.info("xml source url: %s", url)

    try:
        resp = requests.get(url)
        logging.info('response code: %s', resp.status_code)
        logging.info("saving to file")
        with open('temp.xml', 'wb') as f: 
            f.write(resp.content)
    except requests.exceptions.RequestException as e:
        logging.info(e)
        logging.info("Failed. Never mind... we'll try again in a bit.")
        return

    logging.info("parsing xml ...")
    xml_doc = xml.dom.minidom.parse('temp.xml')
    newsitems = xml_doc.getElementsByTagName('item')
    stories_list = []
    for item in newsitems:
        story_dict = {}
        title = item.getElementsByTagName('title')[0].childNodes[0].data
        description = item.getElementsByTagName('description')[0].childNodes[0].data
        link = item.getElementsByTagName('guid')[0].childNodes[0].data
        logging.debug("Checking headline: %s - %s", title, link)
        if reg.search(title):
            logging.info("Match found: %s. %s", title, description)
            story_dict['headline'] = title
            story_dict['description'] = description
            story_dict['url'] = link
            stories_list.append(story_dict)
        else:
            logging.debug("No matches found")
    return stories_list

def update_stories_in_db(stories_list):
    logging.info('Updating stories in db, if required ...')

    for story in stories_list:
        logging.debug("working on story: ")
        logging.debug(story)
        logging.debug("checking if already reported")

        # check for url to remove reposts
        url = story['url']
        already_there_url = collection.count_documents({"url": url})
        if already_there_url == 0:
            logging.info("Looks new, adding story to db collection ...")
            story['timestamp'] = time.time()
            insert_result = collection.insert_one(story)
            if insert_result.acknowledged:
                if Config.DISCORD_NOTIFY == 'True':
                    do_discord_notification(story)
                if Config.TWITTER_NOTIFY == 'True':
                    do_twitter_notification(story)
        else:
            logging.info("Story already in DB ... " + url )


def do_twitter_notification(story):
    logging.info("Doing a Twitter notification...")
    embed_url = story['url']
    response = client.create_tweet(
            text=Config.TWITTER_STATUS_PREFIX + " " + story['headline']+ "  " + embed_url
            )
    print(f"https://twitter.com/user/status/{response.data['id']}")
    logging.info("Twitter notification complete.")
    logging.info("Tweeted: " + story['headline'])


def do_discord_notification(story):
    logging.info("Doing a discord notification...")
    logging.info(story)

    embed_headline = story['headline']
    embed_url = story['url']
    embed_summary = story['description']

    url = Config.DISCORD_WEBHOOK_URL

    data = {"content": Config.DISCORD_CONTENT, "username": Config.DISCORD_USERNAME, "embeds": []}

    embed = {"description": embed_summary,
             "title": embed_headline,
             "url": embed_url,
             "footer": {'text': embed_url}}
    data["embeds"].append(embed)

    result = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.info(err)
    else:
        logging.info("Notification delivered successfully, code {}.".format(result.status_code))

    logging.info("Done the discord notification:")


def main():


    urls=Config.SOURCE_XML.split()
    logging.info("URLs: %s", urls)

    while True:
        # the main bit
        for url in urls:

            get_stories_list = scrape_bbc_news_xml(url)

            logging.info("We have %s stories to check against the DB", str(len(get_stories_list)))

            # chuck results in db
            if get_stories_list:
                update_stories_in_db(get_stories_list)
            else:
                logging.info("No new stories found.")

        # loop delay
        logging.info("Waiting for next run.")
        time.sleep(int(Config.REPEAT_DELAY))

if __name__ == '__main__':
    main()
