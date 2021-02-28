# RedditJolygolfBot
Reddit bot for [r/Jolygolf](https://www.reddit.com/r/Jolygolf/). Subreddit about Russian blogger Alexei Shevcov. Posts images, polls, links from different sources (incl. VK, YouTube)

[![RedditJolygolfBot](https://jolybot.utidteam.com/jolygolf_banner.png)](https://reddit.com/r/jolygolf)

## How to use it?
If you want to use it for your subreddit, check [this step-by-step tutorial](HowToSetup.md)

## Short overview
### Root files
**NaPriemeUShevcova.php, AlexeyShevcov.php, JolyBell.php, BananoviyRai.php**\
These PHP scripts are executing **api_request.php** script with specified parameters. These files sheduled in crontab

**api_request.php**\
This PHP script work with VKontakte API and filtering data from fetched response\
Required parameters:
* `--id` is id of vkontakte group or vkontakte user which replaces {id} variable in vk_api.txt (e.g. `-88245281`)
* `--sourcespec` is any word or term you use to split different sources (e.g. `NaPriemeUShevcova`, `BananoviyRai`)
* `--deftitle` is default title for post where _ is replaced by space (e.g. `На_приеме_у_Шевцова`)
* `--sourcename` is name of source where _ is replaced by space (used in flairs, e.g. `:i:_На_приеме_у_Шевцова`)
* `--sourceshort` is short name of source where _ is replaced by space (used in flairs, e.g. `:i:Паблик`)

Optional parameters:
* `--flairid` is flair id on reddit (e.g. `2ea55bd8-e3e6-11ea-8a5c-0e7cceef0c57`)
* `--offset` is offset which replaces {offset} variable in vk_api.txt (e.g. `2`)
* `--ignorecache` is set when you want to ignore cached id of last post (it has no value)
* `--skipdownload` is set when you want to skip video downloading (it has no value)

**reddit_post.py**\
This Python scripts work with Reddit API and posts submissions and comments to sub. Parameters should be in the same order as api_request.php but without names (`--id`, `--deftitle` etc). If you don't want to add flair to post, use `not-specified` instead of flair id.

**ItpediaYoutube.php**\
This script executing **youtube_api.php** with specified parameters to get video from [Itpedia's channel](https://www.youtube.com/user/itpediachannel). It sheduled in cron.

**youtube_api.php**\
This script makes request to YouTube API to get last video in playlist.

**reddit_youtube_video_post.py**\
This script post link to video to subreddit

**AlexeyShevcov_last_posted_id.txt, NaPriemeUShevcova_last_posted_id.txt, ItpediaYoutube_last_posted_id.txt, JolyBell_last_posted_id.txt, BananoviyRai_last_posted_id.txt**\
Files to compare fetched ID from API to cached (last post), used by **api_request.php** files

### /logs
Directory for logging

### /configs
Check examples in [/configs/](/configs/)

**bot_settings.conf**
```yaml
{
  "bot_username": "Reddit account login",
  "bot_useragent": "Reddit will ban you if you keep this empty, usually looks like r/SUBREDDIT bot by /u/USERNAME",
  "subreddit": "Subreddit name without r/",
  "is_moderator": true or false
}
```
if you set "is_moderator" to false, [reddit_post.py](/reddit_post.py) won't set flair and spoiler tag, approve post, post a comment

**regular_source_settings.conf**
```yaml
{
    "flair_formats": ["Formats with {source_name}, {short_source_name}, {likes}, {comments}, {reposts}, {views} like these",
                     "{source_name} | {likes} :l: | {comments}:c: | {reposts}:r: | {views}:e:",
                     "{short_source_name} | {likes}:l: | {comments}:c: | {reposts}:r: | {views}:e:"],
    "upload_videos_to_reddit": if set to false, bot posts link to video,
    "max_video_resolution": "360, 480, 720 or 1080",
    "gif_link_hint": "It appears when the post has GIF file attached (api_request.php:95)",
    "ads_words": ["posts with these words", "will be ignored"],
    "away_link_text": "Text of link to original post  (reddit_post.py:145)",
    "away_link_format": "Link with {urlid}, {src_id} and {sourcespec}",
    "full_text_hint": "Hint label before full text of original post"
}
```

**spoilers_settings.conf**
```yaml
{
  "spoilers_words": ["posts with these words", "will be archived or/and spoiler-tagged"],
  "archive_spoilers_posts": true or false,
  "spolertag_spoilers_posts": true or false
}
```


**youtube_source_settings.conf**
```yaml
{
    "new_video_hint": "title for submission with {channelname}"
}
```

### /resources
Data to transfer between **api_request.php** and **reddit_post.py** scripts

#### /resources/data
**NaPriemeUShevcova.txt, AlexeyShevcov.txt, ItpediaYoutube.txt, JolyBell.txt, BananoviyRai.txt**\
Data format:
```yaml
{
    "type": "text OR img OR gif OR video OR poll",
    "poll_data": ["ANSWER1","ANSWER2","ANSWER3"],
    "video_data": "FOR VIDEO TYPE, USERID_VIDEOID",
    "likes_count": 1090,
    "reposts_count": 43,
    "views_count": 11613,
    "title": "BASE64-ENCODED TEXT",
    "images_count": 1,
    "post_id": "USERID_POSTID"
}
```

#### /resources/picture
**NaPriemeUShevcova.jpg, AlexeyShevcov.jpg, ItpediaYoutube.jpg, JolyBell.jpg, BananoviyRai.jpg**\
Pictures in posts in most available quality, downloaded by **api_request.php** script from VK server to later upload to reddit server via PRAW

#### /resources/video
**NaPriemeUShevcova_thumbnail.jpg, AlexeyShevcov_thumbnail.jpg, ItpediaYoutube_thumbnail.jpg, JolyBell_thumbnail.jpg, BananoviyRai_thumbnail.jpg**\
Thumbnail of the video in max resolution available, downloaded by **api_request.php** script from VK server

**NaPriemeUShevcova_video.mp4, AlexeyShevcov_video.mp4, ItpediaYoutube_video.mp4, JolyBell_video.mp4, BananoviyRai_video.mp4**\
Video in 360p downloaded by **api_request.php** script to upload on Reddit via PRAW

### /secrets
For private data such as passwords, API keys, directories

#### /secrets/reddit_client_id.txt
Client ID which reddit generates on reddit apps page

#### /secrets/reddit_client_secret.txt
Client secrete which reddit generates on reddit apps page

#### /secrets/reddit_client_password.txt
Account password with which app was created on reddit apps page

#### /secrets/vk_api.txt
VK API endpoint. May contain {id}, {offset} text variables. Read more in [HowToSetup.md](/HowToSetup.md)

#### /secrets/work_dir.txt
Path to repository root (e.g. `/etc/VityaSchel/RedditJolygolfBot/`)

#### /secrets/youtube_api.txt
YouTube API endpoint. Read more in [HowToSetup.md](HowToSetup.md)
