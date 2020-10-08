import praw
import base64
import re
import sys

work_dir = sys.argv[0].split("JolyBell.py")[0];

client_id_f = open(work_dir+"secrets/reddit_client_id.txt", mode="r", encoding="utf-8")
client_id_s = client_id_f.read();
client_secret_f = open(work_dir+"secrets/reddit_client_secret.txt", mode="r", encoding="utf-8")
client_secret_s = client_secret_f.read();
password_f = open(work_dir+"secrets/reddit_password.txt", mode="r", encoding="utf-8")
password_s = password_f.read();

f = open(work_dir+"resources/data/JolyBell.txt", mode="r", encoding="utf-8")
infs = f.read().split(';', 7);

reddit = praw.Reddit(client_id=client_id_s,
                     client_secret=client_secret_s,
                     password=password_s,
                     user_agent='utidteam.com bot by /u/vitya_schel',
                     username='Jolygolf_bot')

type = infs[0]
originalTitle = base64.b64decode(infs[6]).decode('utf-8');
leaveFullComment = 0
if(type == 'img'):
    if(len(originalTitle) < 300):
        title = originalTitle;
    else:
        title = "Jolybell (текст записи в комментариях)"
        leaveFullComment = 1
    image = work_dir+'resources/picture/JolyBell.jpg'
    submission = reddit.subreddit('jolygolf').submit_image(title, image)
else:
    if(type.split(":")[0] == "poll"):
        title = 'Jolybell'
        submission = reddit.subreddit('jolygolf').submit_poll(title, selftext= originalTitle, options=type.split(":")[1].split("#"), duration=3)
        leaveFullComment = 0;
    else:
        title = 'Jolybell'
        submission = reddit.subreddit('jolygolf').submit(title, selftext=originalTitle)
        leaveFullComment = 0;

likes = str(infs[2]);
reposts = str(infs[3]);
comments = str(infs[4]);
views = str(infs[5]);

source = "JolyBell"
flairtext = "{source} | {l} :l: | {r} :r: | {v} :e:".format(source=source, l=likes, r=reposts, v=views)
if(len(flairtext) > 64):
    flairtext = "{source} |{l}:l: | {r}:r: | {v}:e:".format(source=source, l=likes, r=reposts, v=views)
    if(len(flairtext) > 64):
        source = "JB"
        flairtext = "{source} | {l}:l: | {r}:r: | {v}:e:".format(source=source, l=likes, r=reposts, v=views)

submission.flair.select("2ea55bd8-e3e6-11ea-8a5c-0e7cceef0c57", flairtext)


urlID = infs[7].split("_")[1]
urlFull = "https://jolybot.utidteam.com/away.php?url={urlid}&source=jb".format(urlid=urlID)
if(leaveFullComment == 0):
    comment = submission.reply("[Запись ВКонтакте]({urlFull})".format(urlFull=urlFull))
else:
    infs = originalTitle.splitlines()
    txt = "";
    for line in infs:
        txt += '\n> {l}'.format(l=line)

    txt = re.sub("(> \n)", "", txt);

    comment = submission.reply("[Запись ВКонтакте]({urlFull}) \n\nПолный текст записи: {txt}".format(urlFull=urlFull, txt=txt))
comment.mod.distinguish(how='yes', sticky=True)
comment.mod.approve();
submission.mod.approve();
