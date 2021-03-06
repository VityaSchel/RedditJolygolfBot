# How to setup this bot
Make sure you have PHP ≥ 7.2, Python 3, last version of [PRAW](https://praw.readthedocs.io/en/latest/), [youtube-dl](https://en.wikipedia.org/wiki/Youtube-dl) installed on Linux (tested on Ubuntu)
Also make sure all scripts can be executed by python and user that executing php
1. Go to [Reddit apps](https://www.reddit.com/prefs/apps/) and create new app with type of script. You can set any about uri and redirect uri, it won't change anything.
2. Clone this repository from github to your server
3. Delete any sources you want. Source is 1 \*.php file and 1 \*_last_posted.txt file where \* is the same name.
4. Add any sources you want. Source is \*.php file that you shedule which executing **api_request.php** file with specified paramenters.
5. Paste app id (it's under "personal use script" label) in /secrets/reddit_client_id.txt, app secret in /secrets/reddit_client_secret.txt, account password in /secrets/reddit_password.txt and path to the root of this repository in /secrets/work_dir.txt
6. Now you have to find API endpoint URL to get posts from original source. In case you using VKontakte, it should be something like this `https://api.vk.com/method/wall.get?access_token=YourAccessToken&v=Version&owner_id={id}&offset={offset}`. {id} is required variable, don't remove it from URL. You may remove {offset} variable from URL. You can reorder variables in URL. Set access token and version, then place URL in /secrets/vk_api.txt\
If you don't want to use youtube API, delete **youtube_api.php** and **reddit_youtube_video_post.py** files, otherwise, paste youtube api endpoint to /secrets/youtube_api.txt, it should be something like this `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=1&key={your api key}&playlistId={channel uploads playlist id}`, remove {channel uploads playlist id} from this url to append it later in **youtube_api.php**
7. Change configs in /configs/. You can find explanation in [README.md](/README.md#configs)
8. Don't forget to approve account, from which you created app in first step in subreddit settings and make it mod of selected subreddit, otherwise reddit will give you 8 minutes cooldown every time you post something or comment.
9. Shedule job to execute \*.php script (step 4) every 30 minutes

# How it all works
**api_request.php** script makes GET request to API and then gets information from response\
it writes picture to /resources/picture/\*.jpg and info such as post text and stats to /resources/data/\*.txt\
if post's type is video which was uploaded directly to vk.com, video lengths ≤ 600 seconds, **api_request.php** downloads video from VK using youtube-dl to /resources/video/\*_video.mp3 with maximum quality available (up to 480p, you can change it in regular_source_settings.conf) and thumbnail to /resources/video/\*_thumbnail.jpg
then it runs **reddit_post.py** by executing command `python3 {work_dir const}/reddit_post.py [source id] [source spec] [default title] [source name] [short source name] [flair_id]`\
you can find explanation of these parameters in [README.md](README.md)
**reddit_post.py** script reads 6 text files in /secrets/ folder, establish connection to reddit API\
it decides what should post look like (text/image/poll/video)\
then it submit post and comment to reddit\

Take a moment to read all scripts to fully understand how it works. It's also worth looking at the source code, at least in [api_request.php](api_request.php) and [reddit_post.py](reddit_post.py)
