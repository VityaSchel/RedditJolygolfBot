# coding=utf-8
import praw
import base64
import re
import sys
import logging
import json

WORK_DIR = sys.argv[0].split("reddit_post.py")[0][:-1]

logging.basicConfig(filename=WORK_DIR + '/logs/reddit_post.log', level=logging.DEBUG)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

try:
    def get_flair(format_index):
        formats = ["{source_name} | {likes} :l: | {comments} :c: | {reposts} :r: | {views} :e:",
                   "{source_name} | {likes}:l: | {comments}:c: | {reposts}:r: | {views}:e:",
                   "{short_source_name} | {likes}:l: | {comments}:c: | {reposts}:r: | {views}:e:"]
        # each of this is shorter than the other one, this way we achieve 64-characters-length flair
        # if change length of array above, don't forget to change number of formats in for cycle

        new_flair_text = formats[format_index].format(source_name=reddit_submission.src_name_full,
                                                      short_source_name=reddit_submission.src_name_short,
                                                      likes=source_post.likes_count,
                                                      comments=source_post.comments_count,
                                                      reposts=source_post.reposts_count,
                                                      views=source_post.views_count)
        return new_flair_text

    class RedditSubmission:
        def __init__(self, source_specification_code, source_name_full, source_name_short, flairid):
            self.src_spec = source_specification_code
            self.src_name_full = source_name_full.replace("_", " ")
            self.src_name_short = source_name_short.replace("_", " ")
            self.flair_id = flairid


    class FetchedPost:
        def __init__(self, post_type, post_likes, post_reposts, post_comments,
                     post_views, post_title, source_post_id):
            self.post_type = post_type
            if "poll_data" in source_post_raw:
                self.poll_data = source_post_raw['poll_data']
            if "video_data" in source_post_raw:
                self.video_data = source_post_raw['video_data']
            self.likes_count = post_likes
            self.reposts_count = post_reposts
            self.comments_count = post_comments
            self.views_count = post_views
            self.title = base64.b64decode(post_title).decode('utf-8')
            self.src_post_id = source_post_id.split("_")[1]

    bot_id = open(WORK_DIR + "/secrets/reddit_client_id.txt", mode="r", encoding="utf-8").read()
    bot_secret = open(WORK_DIR + "/secrets/reddit_client_secret.txt", mode="r", encoding="utf-8").read()
    bot_password = open(WORK_DIR + "/secrets/reddit_password.txt", mode="r", encoding="utf-8").read()

    reddit_api = praw.Reddit(client_id=bot_id,
                             client_secret=bot_secret,
                             password=bot_password,
                             user_agent='r/Jolygolf bot by /u/Vitya_Schel',
                             username='Jolygolf_bot')

    reddit_submission = RedditSubmission(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    source_post_raw = json.loads(open(WORK_DIR + "/resources/data/" + reddit_submission.src_spec + ".txt", mode="r",
                           encoding="utf-8").read())
    source_post = FetchedPost(source_post_raw['type'], source_post_raw['likes_count'], source_post_raw['reposts_count'],
                              source_post_raw['comments_count'], source_post_raw['views_count'],
                              source_post_raw['title'], source_post_raw['post_id'])

    post_comment_with_source_text = False
    archive_submission = False
    if source_post.post_type == "img":
        if len(source_post.title) < 300:
            title = source_post.title
        else:
            title = reddit_submission.src_name_full + " (текст записи в комментариях)"
            post_comment_with_source_text = True
        image = WORK_DIR + '/resources/picture/' + reddit_submission.src_spec + '.jpg'
        submitted_instance = reddit_api.subreddit('jolygolf').submit_image(title, image)
    else:
        if source_post.post_type == "poll":
            title = reddit_submission.src_name_full
            submitted_instance = reddit_api.subreddit('jolygolf').submit_poll(title, selftext=source_post.title,
                                                                              options=source_post.poll_data[:6],
                                                                              duration=3)
        else:
            if source_post.post_type == "video":
                if len(source_post.title) < 300:
                    title = source_post.title
                else:
                    title = source_post.title[0:297]+"..."
                    post_comment_with_source_text = True

                submitted_instance = reddit_api.subreddit('jolygolf').submit_video(
                                                title,
                                                WORK_DIR+"/resources/video/"+reddit_submission.src_spec+"_video.mp4",
                                                False,
                                                WORK_DIR+"/resources/video/"+reddit_submission.src_spec+"_thumbnail.jpg")
            else:
                # text type or unsupported
                title = reddit_submission.src_name_full
                submitted_instance = reddit_api.subreddit('jolygolf').submit(title, selftext=source_post.title)

    # list of blacklisted words (archive post to avoid spoilers in comments)
    if source_post.title in ["The Last Of Us", "TLOU", "Ласт оф ас", "Тлоу", "Cyberpunk", "Киберпанк"]:
        archive_submission = True

    likes = str(source_post.likes_count)
    reposts = str(source_post.reposts_count)
    comments = str(source_post.comments_count)
    views = str(source_post.views_count)

    if reddit_submission.flair_id != "not-specified":
        # otherwise, not set flair to submission
        flair_text = ""
        for i in range(0, 3):
            flair_text = get_flair(i)
            if len(flair_text) <= 64:
                break

        submitted_instance.flair.select(reddit_submission.flair_id, flair_text)

    # this is optional; you can change it to your domain to analyze links or to direct link
    url_post_id = source_post.src_post_id
    away_link_url = "https://jolybot.utidteam.com/away.php?url={urlid}&source={sourcespec}"
    url_post = away_link_url.format(urlid=url_post_id,
                                    sourcespec=reddit_submission.src_spec)
    if not post_comment_with_source_text:
        comment = submitted_instance.reply("[Запись ВКонтакте]({full_url})".format(full_url=url_post))
    else:
        source_post_text = source_post.title.splitlines()
        reddit_submission_text = ""
        for line in source_post_text:
            reddit_submission_text += '\n> {l}'.format(l=line)

        reddit_submission_text = re.sub("(> \n)", "", reddit_submission_text)

        comment = submitted_instance.reply(
            "[Запись ВКонтакте]({full_url}) \n\nПолный текст записи: {full_text}".format(
                                                                   full_url=url_post, full_text=reddit_submission_text))
    comment.mod.distinguish(how='yes', sticky=True)
    comment.mod.approve()
    submitted_instance.mod.approve()
    if archive_submission == 1:
        submitted_instance.mod.lock()
except RuntimeError as identifier:
    logging.exception('Got exception on main handler')
