import praw
import sys

work_dir = sys.argv[0].split("ItpediaYoutube.py")[0];

client_id_f = open(work_dir+"secrets/reddit_client_id.txt", mode="r", encoding="utf-8")
client_id_s = client_id_f.read();
client_secret_f = open(work_dir+"secrets/reddit_client_secret.txt", mode="r", encoding="utf-8")
client_secret_s = client_secret_f.read();
password_f = open(work_dir+"secrets/reddit_password.txt", mode="r", encoding="utf-8")
password_s = password_f.read();

f = open(work_dir+"resources/data/ItpediaYoutube_last_posted_id.txt", mode="r", encoding="utf-8")
infs = f.read().split(';', 6);

reddit = praw.Reddit(client_id=client_id_s,
                     client_secret=client_secret_s,
                     password=password_s,
                     user_agent='utidteam.com bot by /u/vitya_schel',
                     username='Jolygolf_bot')

if(len(infs[1]) < 300):
    title = infs[1]
else:
    title = "Новое видео на канале Itpedia";
submission = reddit.subreddit('jolygolf').submit(title, url=infs[0], flair_id='6a360654-26d9-11ea-b36f-0ee735f1b64b')
