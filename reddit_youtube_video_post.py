import praw
import sys
import json

WORK_DIR = sys.argv[0].split("reddit_youtube_video_post.py")[0][:-1]
source_spec = sys.argv[1]
source_name = sys.argv[2].replace("_", " ")
flair_id = sys.argv[3]

bot_settings = json.loads(open(WORK_DIR + "/configs/bot_settings.conf", mode="r", encoding="utf-8").read())
spoilers_settings = json.loads(open(WORK_DIR + "/configs/spoilers_settings.conf", mode="r",
                                                                                  encoding="utf-8").read())
youtube_source_settings = json.loads(open(WORK_DIR + "/configs/youtube_source_settings.conf",
                                          mode="r",
                                          encoding="utf-8").read())

bot_id = open(WORK_DIR + "/secrets/reddit_client_id.txt", mode="r", encoding="utf-8").read();
bot_secret = open(WORK_DIR + "/secrets/reddit_client_secret.txt", mode="r", encoding="utf-8").read();
bot_password = open(WORK_DIR + "/secrets/reddit_password.txt", mode="r", encoding="utf-8").read();

reddit_api = praw.Reddit(client_id=bot_id,
                         client_secret=bot_secret,
                         password=bot_password,
                         user_agent=bot_settings['bot_useragent'],
                         username=bot_settings['bot_username'])

video_data = open(WORK_DIR+"/resources/data/"+source_spec+".txt", mode="r", encoding="utf-8").read().split(';', 1)

if(len(video_data[1]) < 300):
    title = video_data[1]
    if title in spoilers_settings['spoilers_words']:
        if spoilers_settings['archive_spoilers_posts']:
            submitted_instance.mod.lock()
        if spoilers_settings['spolertag_spoilers_posts']:
            submitted_instance.mod.spoiler()
else:
    title = youtube_source_settings['new_video_hint'].format(channelname=source_name)

submitted_instance = reddit_api.subreddit(bot_settings['subreddit']).submit(title,
                                                                         url=video_data[0])

if flair_id != "not-specified":
    submitted_instance.flair.select(flair_id)

submitted_instance.mod.approve();
