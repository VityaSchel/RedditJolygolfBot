# RedditJolygolfBot
Бот для сабреддита [r/Jolygolf](https://www.reddit.com/r/Jolygolf/) о видеоблоггере Алексее Шевцове. Умеет постить изображения, опросы, ссылки из разных источников как VK и YouTube

## Краткий обзор
### Корневые файлы
**NaPriemeUShevcova.php, AlexeyShevcov.php, JolyBell.php, BananoviyRai.php**\
Эти PHP скрипты запускают **api_request.php** с особыми параметрами. Их запуск запланирован в cron.

**api_request.php**\
Этот PHP скрипт работает с API Вконтакте и фильтрует информацию из ответа

**reddit_post.py**\
Скрипт Python, работающий с PRAW и публикующий новые посты

**ItpediaYoutube.php**\
Этот скрипт запускает **youtube_api.php** с особыми параметрами для проверки новых видео на [Канале Itpedia](https://www.youtube.com/user/itpediachannel). Запуск запланирован в cron.

**youtube_api.php**\
Этот скрипт обращается к YouTube API, чтобы проверить новые видео в указанном плейлисте

**reddit_youtube_video_post.py**\
Этот скрипт постит ссылки на новые видео в сабреддит

**AlexeyShevcov_last_posted_id.txt, NaPriemeUShevcova_last_posted_id.txt, ItpediaYoutube_last_posted_id.txt, JolyBell_last_posted_id.txt, BananoviyRai_last_posted.txt**\
Файлы для сравнения текущего последнего ID от API и того, что в кеше (последний пост). Используется скриптом **api_request.php**

### logs (директория)
Директория для логов

### /configs
Check examples in [/configs/](/configs/)

**bot_settings.conf**
```yaml
{
  "bot_username": "Логин аккаунта на реддите",
  "bot_useragent": "Реддит может забанить, если оставить это пустым, выглядит так: r/SUBREDDIT bot by /u/USERNAME",
  "subreddit": "Название сабреддита без r/"
}
```

**regular_source_settings.conf**
```yaml
{
    "flair_formats": ["Форматы фалера с {source_name}, {short_source_name}, {likes}, {comments}, {reposts}, {views} like these",
                     "{source_name} | {likes} :l: | {comments}:c: | {reposts}:r: | {views}:e:",
                     "{short_source_name} | {likes}:l: | {comments}:c: | {reposts}:r: | {views}:e:"],
    "upload_videos_to_reddit": если поставлено в false, бот постит ссылку на видео,
    "max_video_resolution": "360, 480, 720 или 1080",
    "gif_link_hint": "Используется когда к посту прикреплена гифка (api_request.php:95)",
    "ads_words": ["записи с этими словами", "будут игнорироваться"],
    "away_link_text": "Текст ссылки на оригинальный пост (reddit_post.py:145)",
    "away_link_format": "Ссылка с {urlid}, {src_id} и {sourcespec}",
    "full_text_hint": "Подсказка перед полным текстом оригинального поста"
}
```

**spoilers_settings.conf**
```yaml
{
  "spoilers_words": ["записи с этими словами", "будут архивированы и/или помечены как спойлер"],
  "archive_spoilers_posts": true или false,
  "spolertag_spoilers_posts": true или false
}
```


**youtube_source_settings.conf**
```yaml
{
    "new_video_hint": "заголовок поста на реддит с {channelname}"
}
```

### resources (директория)
Информация для сообщения между скриптами **api_request.php** и **reddit_post.py**

#### resources/data
**NaPriemeUShevcova.txt, AlexeyShevcov.txt, ItpediaYoutube.txt, JolyBell.txt, BananoviyRai.txt**\
Формат любого из файлов:\
`{"type":"text OR img OR gif OR video OR poll","poll_data":["ANSWER1","ANSWER2","ANSWER3"],"video_url":"FOR VIDEO TYPE, USERID_VIDEOID","likes_count":1090,"reposts_count":43,"views_count":11613,"title":"BASE64-ENCODED TEXT","post_id":"USERID_POSTID"}`

#### resources/picture
**NaPriemeUShevcova.jpg, AlexeyShevcov.jpg, ItpediaYoutube.jpg, JolyBell.jpg, BananoviyRai.jpg**\
Изображения в максимальном качестве, скачанные скриптом **api_request.php** с сервера ВК и позже загруженные на сервер reddit с помощью PRAW

#### resources/video
**NaPriemeUShevcova_thumbnail.jpg, AlexeyShevcov_thumbnail.jpg, ItpediaYoutube_thumbnail.jpg, JolyBell_thumbnail.jpg, BananoviyRai_thumbnail.jpg**\
Превью видео, скачанное **api_request.php** с сервера VK

**NaPriemeUShevcova_video.mp4, AlexeyShevcov_video.mp4, ItpediaYoutube_video.mp4, JolyBell_video.mp4, BananoviyRai_video.mp4**\
Видео в качестве 360p, скачанное **api_request.php** с сервера VK, чтобы загрузить на реддит через PRAW

### secrets (директория)
Для приватной информации: пароли, ключи api, рабочая директория
