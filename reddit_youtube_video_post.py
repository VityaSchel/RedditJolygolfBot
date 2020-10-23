import praw
import sys

WORK_DIR = sys.argv[0].split("reddit_youtube_video_post.py")[0][:-1];
source_spec = sys.argv[1];
source_name = sys.argv[2].replace("_", " ");

bot_id = open(WORK_DIR + "/secrets/reddit_client_id.txt", mode="r", encoding="utf-8").read();
bot_secret = open(WORK_DIR + "/secrets/reddit_client_secret.txt", mode="r", encoding="utf-8").read();
bot_password = open(WORK_DIR + "/secrets/reddit_password.txt", mode="r", encoding="utf-8").read();

reddit_api = praw.Reddit(client_id=bot_id,
                         client_secret=bot_secret,
                         password=bot_password,
                         user_agent='r/Jolygolf bot by /u/Vitya_Schel',
                         username='Jolygolf_bot');

post_data = open(WORK_DIR+"/resources/data/"+source_spec+".txt", mode="r", encoding="utf-8").read().split(';', 6);

if(len(post_data[1]) < 300):
    title = post_data[1];
else:
    title = "Новое видео на канале "+source_name;
submitted_instance = reddit_api.subreddit('jolygolf').submit(title, url=post_data[0], flair_id='6a360654-26d9-11ea-b36f-0ee735f1b64b')
submitted_instance.mod.approve();
