# RedditJolygolfBot
Reddit bot for [r/Jolygolf](https://www.reddit.com/r/Jolygolf/). Subreddit about Russian blogger Alexei Shevcov. Posts images, polls, links from different sources (incl. VK, YouTube)

![RedditJolygolfBot](https://jolybot.utidteam.com/jolygolf_banner.png)

## How to use it?
If you want to use it for your subreddit, check [this step-by-step tutorial](HowToSetup.md)

## Short overview
### Root files
**NaPriemeUShevcova.php, AlexeyShevcov.php, JolyBell.php, BananoviyRai.php**\
These PHP scripts are executing **api_request.php** script with specified parameters. They sheduled in cron.

**api_request.php**\
This PHP script work with VKontakte API and filtering data from fetched response

**reddit_post.py**\
This Python scripts work with Reddit API and posts submissions and comments to sub

**ItpediaYoutube.php**\
This script executing **youtube_api.php** with specified parameters to get video from [Itpedia's channel](https://www.youtube.com/user/itpediachannel). It sheduled in cron.

**youtube_api.php**\
This script makes request to YouTube API to get last video in playlist.

**reddit_youtube_video_post.py**\
This script post link to video to subreddit

**AlexeyShevcov_last_posted_id.txt, NaPriemeUShevcova_last_posted_id.txt, ItpediaYoutube_last_posted_id.txt, JolyBell_last_posted_id.txt, BananoviyRai_last_posted_id.txt**\
Files to compare fetched ID from API to cached (last post), used by **api_request.php** files

### logs (directory)
Directory for logging\
*Ignored in git, do not place anything here*

### resources (directory)
Data to transfer between **api_request.php** and **reddit_post.py** scripts\
*Do not place anything here*

#### resources/data
**NaPriemeUShevcova.txt, AlexeyShevcov.txt, ItpediaYoutube.txt, JolyBell.txt, BananoviyRai.txt**\
Data format:\
`{"type":"text OR img OR gif OR video OR poll","poll_data":["ANSWER1","ANSWER2","ANSWER3"],"video_url":"FOR VIDEO TYPE, USERID_VIDEOID","likes_count":1090,"reposts_count":43,"views_count":11613,"title":"BASE64-ENCODED TEXT","post_id":"USERID_POSTID"}`
*Ignored in git, do not place anything here*

#### resources/picture
**NaPriemeUShevcova.jpg, AlexeyShevcov.jpg, ItpediaYoutube.jpg, JolyBell.jpg, BananoviyRai.jpg**\
Pictures in posts in most available quality, downloaded by **api_request.php** script from VK server to later upload to reddit server via PRAW\
*Ignored in git, do not place anything here*

#### resources/video
**NaPriemeUShevcova_thumbnail.jpg, AlexeyShevcov_thumbnail.jpg, ItpediaYoutube_thumbnail.jpg, JolyBell_thumbnail.jpg, BananoviyRai_thumbnail.jpg**\
Thumbnail of video in max resoultion available, downloaded by **api_request.php** script from VK server\

**NaPriemeUShevcova_video.mp4, AlexeyShevcov_video.mp4, ItpediaYoutube_video.mp4, JolyBell_video.mp4, BananoviyRai_video.mp4**\
Video in 360p downloaded by **api_request.php** script to upload on Reddit via PRAW\

*Игнорируется, ничего не помещайте здесь*

### secrets (directory)
For private data such as passwords, api keys, directories\
*Ignored in git, do not place anything here*
