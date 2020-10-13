# How to setup this bot
Make sure you have php 7.2, python 3 and last version of PRAW installed on linux
1. Go to [Reddit apps](https://www.reddit.com/prefs/apps/) and create new app
2. Clone this repository
3. Delete any sources you want. Source is 1 \*.php file and 1 \*_last_posted.txt file where \* is the same name.
4. Add any sources you want. Source is \*.php file that you shedule which executing **api_request.php** file with specified paramenters.
5. Paste client_id in /secrets/reddit_client_id.txt, client_secret in /secrets/reddit_client_secret.txt, account password in /secrets/reddit_password.txt and path to the root of this repository in /secrets/work_dir.txt
6. Now you have to find API endpoint URL to get posts from original source. In case you using VKontakte, it should be something like this `https://api.vk.com/method/wall.get?access_token={access_token}&v={version}&owner_id={owner_id}`. Remove {owner_id} from this url to append it later in api_request.php script and place URL in /secrets/vk_api.txt\
If you don't want to use youtube API, delete **youtube_api.php** and **reddit_youtube_video_post.py** files, otherwise, paste youtube api endpoint to /secrets/youtube_api.txt, it should be something like this `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=1&key={your api key}&playlistId={channel uploads playlist id}`, remove {channel uploads playlist id} from this url to append it later in **youtube_api.php**
7. Change subreddit from *r/jolygolf* to yours in **reddit_post.py** and **reddit_youtube_video_post.py** scripts
8. Don't forget to approve account, from which you created app in first step in subreddit settings and make it mod of selected subreddit, otherwise reddit will give you 8 minutes cooldown every time you post something or comment.
9. Shedule job to execute \*.php script (step 4) every 30 minutes

# How it all works
**api_request.php** script makes GET request to API and then gets information from response\
it writes picture to /resource/picture/\*.jpg and info such as post text and stats to /resources/data/\*.txt\
then it calls **reddit_post.py** file by executing command `python3 {work_dir const}/reddit_post.py {source name} {flair (source) name} {short flair (source) name}`\
**reddit_post.py** script reads everything from /secrets/ folder, makes connection to reddit\
it decides what should post look like (text/image/poll)\
then it posts submission and comment to reddit\

Take a moment to read all scripts to fully understand how it works. You could also find syntax for arguments and usable comments in code.