import praw
import base64
import re
import sys
import logging
import time

# filepath syntax: work_dir/reddit_post.py NaPriemeUShevcova На_приеме_у_Шевцова Паблик flairid

work_dir = sys.argv[0].split("reddit_post.py")[0];

LOG_FILENAME = work_dir+'logs/reddit_post.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

try:
    source_spec = sys.argv[1];
    source_name = sys.argv[2].replace("_"," ");
    source_name_short = sys.argv[3].replace("_"," ");
    flairid = sys.argv[4];

    client_id_f = open(work_dir+"secrets/reddit_client_id.txt", mode="r", encoding="utf-8")
    client_id_s = client_id_f.read();
    client_secret_f = open(work_dir+"secrets/reddit_client_secret.txt", mode="r", encoding="utf-8")
    client_secret_s = client_secret_f.read();
    password_f = open(work_dir+"secrets/reddit_password.txt", mode="r", encoding="utf-8")
    password_s = password_f.read();

    f = open(work_dir+"resources/data/"+source_spec+".txt", mode="r", encoding="utf-8")
    infs = f.read().split(';', 7);

    reddit = praw.Reddit(client_id=client_id_s,
                         client_secret=client_secret_s,
                         password=password_s,
                         user_agent='utidteam.com bot by /u/vitya_schel',
                         username='Jolygolf_bot')

    type = infs[0]
    originalTitle = base64.b64decode(infs[6]).decode('utf-8');
    leaveFullComment = 0
    archiveRedditPost = 0
    if(type == "img"):
        if(len(originalTitle) < 300):
            title = originalTitle;
        else:
            title = source_name+" (текст записи в комментариях)";
            leaveFullComment = 1;
        image = work_dir+'resources/picture/'+source_spec+'.jpg';
        submission = reddit.subreddit('jolygolf').submit_image(title, image)

        # list of blacklisted words (to avoid spoilers)
        if(title in ["The Last Of Us", "TLOU", "Ласт оф ас", "Тлоу", "Cyberpunk", "Киберпанк"]):
            archiveRedditPost = 1;
    else:
        if(type.split(":")[0] == "poll"):
            title = source_name;
            submission = reddit.subreddit('jolygolf').submit_poll(title, selftext=originalTitle, options=type.split(":")[1].split("#"), duration=3);
        else:
            if(type.split(":")[0] == "video"):
                if(len(originalTitle) < 300):
                    title = originalTitle;
                else:
                    title = originalTitle[0:297]+"...";
                    leaveFullComment = 1;
                video_url_vk_api = "https://vkontakte.ru/video";
                # url actually looks like https://vk.com/video-12345_10
                # where -12345 is group id and 10 is video id
                # but reddit banned vk.com "because of child porn"
                # well anyway, vkontakte.ru is just an old domain name
                # if it ever get banned, use your own domain recirect :)
                submission = reddit.subreddit('jolygolf').submit(title, url=video_url_vk_api+type.split(":")[1]);
                # TODO: change to actual upload to v.reddit.com
            else:
                # text type or unsupported
                title = source_name;
                submission = reddit.subreddit('jolygolf').submit(title, selftext=originalTitle);

    likes = str(infs[2]);
    reposts = str(infs[3]);
    comments = str(infs[4]);
    views = str(infs[5]);

    if(flairid != "not-specified"):
        flairtext = "{source} | {l} :l: | {c} :c: | {r} :r: | {v} :e:".format(source=source_name, l=likes, c=comments, r=reposts, v=views)
        if(len(flairtext) > 64):
            flairtext = "{source} |{l}:l: | {c}:c: | {r}:r: | {v}:e:".format(source=source_name, l=likes, c=comments, r=reposts, v=views)
            if(len(flairtext) > 64):
                flairtext = "{source} | {l}:l: | {c}:c: | {r}:r: | {v}:e:".format(source=source_name_short, l=likes, c=comments, r=reposts, v=views)

        submission.flair.select(flairid, flairtext)

    urlID = infs[7].split("_")[1]
    urlFull = "https://jolybot.utidteam.com/away.php?url={urlid}&source={sourcespec}".format(urlid=urlID, sourcespec=source_spec)
    # this is optional; you can change it to your domain to analize links or to direct link
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
    if(archiveRedditPost == 1):
        submission.mod.lock();
except:
    logging.exception('Got exception on main handler')
