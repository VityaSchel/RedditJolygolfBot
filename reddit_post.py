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
    bot_settings = json.loads(open(WORK_DIR + "/configs/bot_settings.conf", mode="r", encoding="utf-8").read())
    spoilers_settings = json.loads(open(WORK_DIR + "/configs/spoilers_settings.conf", mode="r",
                                                                                      encoding="utf-8").read())
    regular_source_settings = json.loads(open(WORK_DIR + "/configs/regular_source_settings.conf",
                                              mode="r",
                                              encoding="utf-8").read())

    def get_flair():
        formats = regular_source_settings['flair_formats']
        # each of this is shorter than the other one, this way we achieve 64-characters-length flair

        flair_template = ""
        for i in range(0, len(regular_source_settings['flair_formats'])):
            flair_template = formats[i]
            if len(flair_template) <= 64:
                break

        flair_text = flair_template.format(source_name=reddit_submission.src_name_full,
                                           short_source_name=reddit_submission.src_name_short,
                                           likes=source_post.likes_count,
                                           comments=source_post.comments_count,
                                           reposts=source_post.reposts_count,
                                           views=source_post.views_count)
        return flair_text

    class RedditSubmission:
        def __init__(self, source_id, source_specification_code, source_name_full, source_name_short, flairid):
            self.src_id = source_id,
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
                             user_agent=bot_settings['bot_useragent'],
                             username=bot_settings['bot_username'])

    reddit_submission = RedditSubmission(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    source_post_raw = json.loads(open(WORK_DIR + "/resources/data/" + reddit_submission.src_spec + ".txt", mode="r",
                           encoding="utf-8").read())
    source_post = FetchedPost(source_post_raw['type'], source_post_raw['likes_count'], source_post_raw['reposts_count'],
                              source_post_raw['comments_count'], source_post_raw['views_count'],
                              source_post_raw['title'], source_post_raw['post_id'])

    post_comment_with_source_text = False
    submission_contains_spoilers = False
    if source_post.post_type == "img":
        if len(source_post.title) < 300:
            title = source_post.title
        else:
            title = reddit_submission.src_name_full + " (текст записи в комментариях)"
            post_comment_with_source_text = True
        image = WORK_DIR + '/resources/picture/' + reddit_submission.src_spec + '.jpg'
        submitted_instance = reddit_api.subreddit(bot_settings['subreddit']).submit_image(title, image)
    else:
        if source_post.post_type == "poll":
            title = reddit_submission.src_name_full
            submitted_instance = reddit_api.subreddit(bot_settings['subreddit']).submit_poll(title,
                                                                                      selftext=source_post.title,
                                                                                      options=source_post.poll_data[:6],
                                                                                      duration=3)
        else:
            if source_post.post_type == "video":
                if len(source_post.title) < 300:
                    title = source_post.title
                else:
                    title = source_post.title[0:297]+"..."
                    post_comment_with_source_text = True

                if regular_source_settings['upload_videos_to_reddit']:
                    submitted_instance = reddit_api.subreddit(['subreddit']).submit_video(
                                               title,
                                               WORK_DIR+"/resources/video/"+reddit_submission.src_spec+"_video.mp4",
                                               False,
                                               WORK_DIR+"/resources/video/"+reddit_submission.src_spec+"_thumbnail.jpg")
                else:
                    video_url_vk_api = "https://vkontakte.ru/video"
                    submitted_instance = reddit_api.subreddit(bot_settings['subreddit']).submit(
                                                                     title, url=video_url_vk_api+source_post.video_data)

            else:
                # text type or unsupported
                title = reddit_submission.src_name_full
                submitted_instance = reddit_api.subreddit(bot_settings['subreddit']).submit(title,
                                                                                            selftext=source_post.title)

    if source_post.title in spoilers_settings['spoilers_words']:
        submission_contains_spoilers = True

    likes = str(source_post.likes_count)
    reposts = str(source_post.reposts_count)
    comments = str(source_post.comments_count)
    views = str(source_post.views_count)

    if reddit_submission.flair_id != "not-specified":
        submitted_instance.flair.select(reddit_submission.flair_id, get_flair())

    url_post_id = source_post.src_post_id
    away_link_url = regular_source_settings['away_link_format']
    url_post = away_link_url.format(urlid=url_post_id,
                                    src_id=reddit_submission.src_id,
                                    sourcespec=reddit_submission.src_spec)

    if not post_comment_with_source_text:
        comment = submitted_instance.reply("[{away_link_hint}]({full_url})".format(
                                                              full_url=url_post,
                                                              away_link_hint=regular_source_settings['away_link_text']))
    else:
        source_post_text = source_post.title.splitlines()
        reddit_submission_text = ""
        for line in source_post_text:
            reddit_submission_text += '\n> {l}'.format(l=line)

        reddit_submission_text = re.sub("(> \n)", "", reddit_submission_text)

        comment = submitted_instance.reply(
            "[{away_link_hint}]({full_url}) \n\n{full_text_hint}: {full_text}".format(
                                                               away_link_hint=regular_source_settings['away_link_text'],
                                                               full_url=url_post,
                                                               full_text_hint=regular_source_settings['full_text_hint'],
                                                               full_text=reddit_submission_text))
    comment.mod.distinguish(how='yes', sticky=True)
    comment.mod.approve()
    submitted_instance.mod.approve()
    if submission_contains_spoilers:
        if spoilers_settings['archive_spoilers_posts']:
            submitted_instance.mod.lock()
        if spoilers_settings['spolertag_spoilers_posts']:
            submitted_instance.mod.spoiler()
except RuntimeError as identifier:
    logging.exception('Got exception on main handler')
