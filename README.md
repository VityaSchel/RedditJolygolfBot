# RedditJolygolfBot
Reddit bot for [r/Jolygolf](https://www.reddit.com/r/Jolygolf/). Subreddit about Russian blogger Alexei Shevcov. Posts images, polls, links from different sources (incl. VK, YouTube)

## Short overview
### Root files
**NaPriemeUShevcova.php, AlexeyShevcov.php, JolyBell.php**
PHP scripts are working with VKontakte API and filtering data from fetched response

**NaPriemeUShevcova.py, AlexeyShevcov.py, JolyBell.py**
Python scripts are working with Reddit API and posts submissions and comments to sub

**ItpediaYoutube.php**
This script makes request to YouTube API to get last video on [Itpedia's channel](https://www.youtube.com/user/itpediachannel)

**ItpediaYoutube.py**
This script post link to video to subreddit

**AlexeyShevcov_last_posted_id.txt, NaPriemeUShevcova_last_posted_id.txt, ItpediaYoutube_last_posted_id.txt, JolyBell_last_posted_id.txt**
Files to compare fetched ID from API to cached (last post), used by \*.php files

### logs (directory)
Directory for logging\
*Ignored in git, do not place anything here*

### resources (directory)
Data to transfer between \*.php and \*.py scripts\
*Do not place anything here*

#### resources/data
**NaPriemeUShevcova.txt, AlexeyShevcov.txt, ItpediaYoutube.txt, JolyBell.txt**
Data format:\
`{type(text,poll:..#..,img)};{image url in VK server};{likes count};{reposts count};{comments count};{views count};{title in UTF-8 encoded in base64};{id in vk groupid_postid}`\
*TODO: Use JSON*\
*Ignored in git, do not place anything here*

#### resources/picture
**NaPriemeUShevcova.jpg, AlexeyShevcov.jpg, ItpediaYoutube.jpg, JolyBell.jpg**
Pictures in posts in most available quality, downloaded by \*.php script from VK server to later upload to reddit server via PRAW\
*Ignored in git, do not place anything here*

### secrets (directory)
For private data such as passwords, api keys, directories\
*Ignored in git, do not place anything here*
