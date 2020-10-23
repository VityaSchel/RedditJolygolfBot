# coding=utf-8
import praw
import base64
import re
import sys
import logging

WORK_DIR = sys.argv[0].split("reddit_post.py")[0][:-1];

logging.basicConfig(filename=WORK_DIR + '/logs/reddit_post.log', level=logging.DEBUG)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

try:
    class RedditSubmission:
        def __init__(self, source_specification_code, source_name_full, source_name_short, flairid):
            self.src_spec = source_specification_code;
            self.src_name_full = source_name_full.replace("_", " ");
            self.src_name_short = source_name_short.replace("_", " ");
            self.flair_id = flairid;


    class FetchedPost:
        def __init__(self, post_type, image_url, likes, reposts, comments, views, title, source_post_id):
            post_type_field = post_type.split(":");
            # TODO: split post type and extra data to different field, also data needs to be in JSON
            self.post_type = post_type_field[0];
            if(len(post_type_field) > 1):
                self.extra_data = post_type_field[1];
            self.image_url = image_url;
            self.likes_count = likes;
            self.reposts_count = reposts;
            self.comments_count = comments;
            self.views_count = views;
            self.title = base64.b64decode(title).decode('utf-8');
            self.src_post_id = source_post_id.split("_")[1];


    reddit_submission = RedditSubmission(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]);

    bot_id = open(WORK_DIR + "/secrets/reddit_client_id.txt", mode="r", encoding="utf-8").read();
    bot_secret = open(WORK_DIR + "/secrets/reddit_client_secret.txt", mode="r", encoding="utf-8").read();
    bot_password = open(WORK_DIR + "/secrets/reddit_password.txt", mode="r", encoding="utf-8").read();

    reddit_api = praw.Reddit(client_id=bot_id,
                             client_secret=bot_secret,
                             password=bot_password,
                             user_agent='r/Jolygolf bot by /u/Vitya_Schel',
                             username='Jolygolf_bot');

    source_post_raw = open(WORK_DIR + "/resources/data/" + reddit_submission.src_spec + ".txt", mode="r",
                           encoding="utf-8").read().split(';', 7);
    source_post = FetchedPost(source_post_raw[0], source_post_raw[1], source_post_raw[2], source_post_raw[3],
                              source_post_raw[4], source_post_raw[5], source_post_raw[6], source_post_raw[7]);

    post_comment_with_source_text = False;
    archive_submission = False;
    if source_post.post_type == "img":
        if len(source_post.title) < 300:
            title = source_post.title;
        else:
            title = reddit_submission.src_name_full + " (текст записи в комментариях)";
            post_comment_with_source_text = True;
        image = WORK_DIR + '/resources/picture/' + reddit_submission.src_spec + '.jpg';
        submitted_instance = reddit_api.subreddit('jolygolf').submit_image(title, image);
    else:
        if source_post.post_type == "poll":
            title = reddit_submission.src_name_full;
            submitted_instance = reddit_api.subreddit('jolygolf').submit_poll(title, selftext=source_post.title,
                                                                              options=source_post.extra_data.split("#"),
                                                                              duration=3);
        else:
            if source_post.post_type == "video":
                if len(source_post.title) < 300:
                    title = source_post.title;
                else:
                    title = source_post.title[0:297]+"...";
                    post_comment_with_source_text = True;

                video_url_vk_api = "https://vkontakte.ru/video";
                # url actually looks like https://vk.com/video-12345_10
                # where -12345 is group id and 10 is video id
                # but reddit banned vk.com "because of child porn"
                # well anyway, vkontakte.ru is just an old domain name
                # if it ever get banned, use your own domain redirect :)
                # TODO: change to actual upload to v.reddit.com
                submitted_instance = reddit_api.subreddit('jolygolf').submit(title,
                                                                         url=video_url_vk_api + source_post.extra_data);
            else:
                # text type or unsupported
                title = reddit_submission.src_name_full;
                submitted_instance = reddit_api.subreddit('jolygolf').submit(title, selftext=source_post.title);

    # list of blacklisted words (archive post to avoid spoilers in comments)
    if source_post.title in ["The Last Of Us", "TLOU", "Ласт оф ас", "Тлоу", "Cyberpunk", "Киберпанк"]:
        archive_submission = True;

    likes = str(source_post.likes_count);
    reposts = str(source_post.reposts_count);
    comments = str(source_post.comments_count);
    views = str(source_post.views_count);

    if (reddit_submission.flair_id != "not-specified"):
        flairtext = "{source} | {l} :l: | {c} :c: | {r} :r: | {v} :e:".format(source=source_post.title,
                                                        l=source_post.likes_count, c=source_post.comments_count,
                                                        r=source_post.reposts_count, v=source_post.views_count);
        if (len(flairtext) > 64):
            flairtext = "{source} |{l}:l: | {c}:c: | {r}:r: | {v}:e:".format(source=source_post.title,
                                                        l=source_post.likes_count, c=source_post.comments_count,
                                                        r=source_post.reposts_count, v=source_post.views_count);
            if (len(flairtext) > 64):
                flairtext = "{source} | {l}:l: | {c}:c: | {r}:r: | {v}:e:".format(source=source_post.title,
                                                        l=source_post.likes_count, c=source_post.comments_count,
                                                        r=source_post.reposts_count, v=source_post.views_count);

        submitted_instance.flair.select(reddit_submission.flair_id, flairtext)

    # this is optional; you can change it to your domain to analyze links or to direct link
    url_post_id = source_post.src_post_id;
    url_post = "https://jolybot.utidteam.com/away.php?url={urlid}&source={sourcespec}".format(urlid=url_post_id,
                                                                                sourcespec=reddit_submission.src_spec);
    if post_comment_with_source_text == True:
        comment = submitted_instance.reply("[Запись ВКонтакте]({urlFull})".format(urlFull=urlFull))
    else:
        source_post_text = source_post.title.splitlines()
        reddit_submission_text = "";
        for line in source_post_text:
            reddit_submission_text += '\n> {l}'.format(l=line)

        reddit_submission_text = re.sub("(> \n)", "", reddit_submission_text);

        comment = submitted_instance.reply(
            "[Запись ВКонтакте]({full_url}) \n\nПолный текст записи: {full_text}".format(full_url=url_post,
                                                                                  full_text=reddit_submission_text));
    comment.mod.distinguish(how='yes', sticky=True)
    comment.mod.approve();
    submitted_instance.mod.approve();
    if archive_submission == 1:
        submitted_instance.mod.lock();
except:
    logging.exception('Got exception on main handler')
