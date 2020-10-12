import praw
import sys

# filepath syntax: work_dir/reddit_youtube_video_post.py ItpediaYoutube itpedia

work_dir = sys.argv[0].split("reddit_youtube_video_post.py")[0];
source_spec = sys.argv[1];
source_name = sys.argv[2].replace("_", " ");

client_id_f = open(work_dir+"secrets/reddit_client_id.txt", mode="r", encoding="utf-8")
client_id_s = client_id_f.read();
client_secret_f = open(work_dir+"secrets/reddit_client_secret.txt", mode="r", encoding="utf-8")
client_secret_s = client_secret_f.read();
password_f = open(work_dir+"secrets/reddit_password.txt", mode="r", encoding="utf-8")
password_s = password_f.read();

f = open(work_dir+"resources/data/"+source_spec+"_last_posted_id.txt", mode="r", encoding="utf-8")
infs = f.read().split(';', 6);

reddit = praw.Reddit(client_id=client_id_s,
                     client_secret=client_secret_s,
                     password=password_s,
                     user_agent='utidteam.com bot by /u/vitya_schel',
                     username='Jolygolf_bot')

if(len(infs[1]) < 300):
    title = infs[1]
else:
    title = "Новое видео на канале "+source_name;
submission = reddit.subreddit('jolygolf').submit(title, url=infs[0], flair_id='6a360654-26d9-11ea-b36f-0ee735f1b64b')
