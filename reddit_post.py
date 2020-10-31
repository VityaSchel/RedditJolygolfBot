# coding=utf-8
import praw
import base64
import re
import sys
import logging
import json

WORK_DIR = sys.argv[0].split("reddit_post.py")[0][:-1]

reddit_api = None
original_post_source = None
original_post_raw = None
original_post = None
reddit_submission = None
url_post = None

bot_settings = json.loads(open(WORK_DIR + "/configs/bot_settings.conf", mode="r", encoding="utf-8").read())
spoilers_settings = json.loads(open(WORK_DIR + "/configs/spoilers_settings.conf", mode="r",
                                    encoding="utf-8").read())
regular_source_settings = json.loads(open(WORK_DIR + "/configs/regular_source_settings.conf",
                                          mode="r",
                                          encoding="utf-8").read())


class RedditSubmission:
    def __init__(self, post_title, post_a_comment, submission):
        self.title = post_title,
        self.post_comment_with_source_text = post_a_comment
        self.submission = submission


class OriginalPostSource:
    def __init__(self, source_id, source_specification_code, source_name_full, source_name_short):
        self.src_id = source_id,
        self.src_spec = source_specification_code
        self.src_name_full = source_name_full.replace("_", " ")
        self.src_name_short = source_name_short.replace("_", " ")


class FetchedPost:
    def __init__(self, post_type, post_likes, post_reposts, post_comments, post_views, post_title,
                 post_attachments_count, source_post_id, flairid):
        self.post_type = post_type
        if "poll_data" in original_post_raw:
            self.poll_data = original_post_raw['poll_data']
        if "video_data" in original_post_raw:
            self.video_data = original_post_raw['video_data']
        self.likes_count = post_likes
        self.reposts_count = post_reposts
        self.comments_count = post_comments
        self.views_count = post_views
        self.text = base64.b64decode(post_title).decode('utf-8')
        self.attachments_count = post_attachments_count
        self.src_post_id = source_post_id.split("_")[1]
        self.flair_id = flairid


def get_flair():
    global regular_source_settings
    global original_post
    global original_post_source

    flair_formats = regular_source_settings['flair_formats']
    flair_template = ""
    for i in range(len(flair_formats)):
        flair_template = flair_formats[i].format(source_name=original_post_source.src_name_full,
                                                 short_source_name=original_post_source.src_name_short,
                                                 likes=original_post.likes_count,
                                                 comments=original_post.comments_count,
                                                 reposts=original_post.reposts_count,
                                                 views=original_post.views_count)
        reddit_max_flair_length = 64
        if len(flair_template) <= reddit_max_flair_length:
            break
    return flair_template


def get_title():
    global reddit_submission
    global original_post

    if len(original_post.text) < 300:
        return original_post.text
    else:
        reddit_submission.post_comment_with_source_text = True
        return original_post_source.src_name_full + " (текст записи в комментариях)"


def submit_pictures():
    global WORK_DIR
    global original_post_source
    global reddit_submission
    global reddit_api
    global bot_settings

    title = get_title()

    if original_post.attachments_count == 1:
        image = WORK_DIR + '/resources/picture/' + original_post_source.src_spec + '_1.jpg'
        reddit_submission.submission = reddit_api.subreddit(bot_settings['subreddit']).submit_image(title, image)
    else:
        images = []
        for i in range(original_post.attachments_count):
            images.append({'image_path': WORK_DIR + '/resources/picture/' + original_post_source.src_spec +
                                                                                               '_' + str(i+1) + '.jpg'})
        reddit_submission.submission = reddit_api.subreddit(bot_settings['subreddit']).submit_gallery(title, images)


def submit_poll():
    global original_post_source
    global reddit_submission
    global reddit_api
    global bot_settings
    global original_post

    title = original_post_source.src_name_full
    reddit_submission.submission = reddit_api.subreddit(bot_settings['subreddit']).submit_poll(title,
                                                                                               selftext=original_post.text,
                                                                                               options=original_post.poll_data[:6],
                                                                                               duration=3)


def submit_video():
    global regular_source_settings
    global reddit_submission
    global reddit_api
    global WORK_DIR
    global original_post
    global bot_settings

    title = get_title()
    if regular_source_settings['upload_videos_to_reddit']:
        reddit_submission.submission = reddit_api.subreddit(['subreddit']).submit_video(title,
                                                                                        WORK_DIR + "/resources/video/" + original_post_source.src_spec + "_video.mp4",
                                                                                        False,
                                                                                        WORK_DIR + "/resources/video/" + original_post_source.src_spec + "_thumbnail.jpg")
    else:
        video_url_vk_api = "https://vkontakte.ru/video"
        reddit_submission.submission = reddit_api.subreddit(bot_settings['subreddit']).submit(title,
                                                                                              url=video_url_vk_api + original_post.video_data)


def submit_text():
    global reddit_submission
    global reddit_api
    global bot_settings
    global original_post

    title = get_title()
    reddit_submission.submission = reddit_api.subreddit(bot_settings['subreddit']).submit(title,
                                                                                          selftext=original_post.text)


def spoilers_test():
    global original_post
    global spoilers_settings
    global reddit_submission

    submission_contains_spoilers = text_contains_any_item(original_post.text, spoilers_settings['spoilers_words'])
    if submission_contains_spoilers:
        if spoilers_settings['archive_spoilers_posts']:
            reddit_submission.submission.mod.lock()
        if spoilers_settings['spolertag_spoilers_posts']:
            reddit_submission.submission.mod.spoiler()


def text_contains_any_item(subject, items):
    for i in range(len(items)):
        if items[i] in subject:
            return True
    return False


def submit_full_text_comment():
    global original_post
    global regular_source_settings
    global url_post

    source_post_text = original_post.text.splitlines()
    reddit_submission_text = ""
    for line in source_post_text:
        reddit_submission_text += '\n> {l}'.format(l=line)
    reddit_submission_text = re.sub("(> \n)", "", reddit_submission_text)

    comment = reddit_submission.submission.reply(
        "[{away_link_hint}]({full_url}) \n\n{full_text_hint}: {full_text}".format(
            away_link_hint=regular_source_settings['away_link_text'],
            full_url=url_post,
            full_text_hint=regular_source_settings['full_text_hint'],
            full_text=reddit_submission_text))

    comment.mod.distinguish(how='yes', sticky=True)
    comment.mod.approve()


def submit_common_comment():
    global url_post
    global regular_source_settings

    comment = reddit_submission.submission.reply("[{away_link_hint}]({full_url})".format(full_url=url_post,
                                                                                         away_link_hint=
                                                                                         regular_source_settings[
                                                                                             'away_link_text']))
    comment.mod.distinguish(how='yes', sticky=True)
    comment.mod.approve()


def get_reddit_api():
    global WORK_DIR
    global bot_settings

    bot_id = open(WORK_DIR + "/secrets/reddit_client_id.txt", mode="r", encoding="utf-8").read()
    bot_secret = open(WORK_DIR + "/secrets/reddit_client_secret.txt", mode="r", encoding="utf-8").read()
    bot_password = open(WORK_DIR + "/secrets/reddit_password.txt", mode="r", encoding="utf-8").read()

    reddit = praw.Reddit(client_id=bot_id,
                         client_secret=bot_secret,
                         password=bot_password,
                         user_agent=bot_settings['bot_useragent'],
                         username=bot_settings['bot_username'])
    return reddit


def initialize():
    global reddit_api
    global original_post_source
    global original_post_raw
    global original_post
    global reddit_submission
    global url_post

    reddit_api = get_reddit_api()

    original_post_source = OriginalPostSource(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    original_post_raw = json.loads(open(WORK_DIR + "/resources/data/" + original_post_source.src_spec + ".txt",
                                        mode="r", encoding="utf-8").read())
    original_post = FetchedPost(original_post_raw['type'],
                                original_post_raw['likes_count'],
                                original_post_raw['reposts_count'],
                                original_post_raw['comments_count'],
                                original_post_raw['views_count'],
                                original_post_raw['title'],
                                original_post_raw['images_count'],
                                original_post_raw['post_id'],
                                sys.argv[5])
    reddit_submission = RedditSubmission("", False, None)

    if original_post.post_type == "img":
        submit_pictures()
    elif original_post.post_type == "poll":
        submit_poll()
    elif original_post.post_type == "video":
        submit_video()
    else:
        submit_text()

    if original_post.flair_id != "not-specified":
        reddit_submission.submission.flair.select(original_post.flair_id, get_flair())

    url_post_id = original_post.src_post_id
    away_link_url = regular_source_settings['away_link_format']
    url_post = away_link_url.format(urlid=url_post_id,
                                    src_id=original_post_source.src_id,
                                    sourcespec=original_post_source.src_spec)

    if not reddit_submission.post_comment_with_source_text:
        submit_common_comment()
    else:
        submit_full_text_comment()

    spoilers_test()

    reddit_submission.submission.mod.approve()


logging.basicConfig(filename=WORK_DIR + '/logs/reddit_post.log', level=logging.DEBUG)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
try:
    initialize()
except RuntimeError as identifier:
    logging.exception('Got exception on main handler')
