# RedditJolygolfBot
Бот для сабреддита [r/Jolygolf](https://www.reddit.com/r/Jolygolf/) о видеоблоггере Алексее Шевцове. Умеет постить изображения, опросы, ссылки из разных источников как VK и YouTube

![RedditJolygolfBot](https://jolybot.utidteam.com/jolygolf_banner.png)

## Как использовать бота?
Если вы хотите использовать бота для своего сабреддита, прочитайте [этот туториал шаг-за-шагом](HowToSetup.md)

## Краткий обзор
### Корневые файлы
**NaPriemeUShevcova.php, AlexeyShevcov.php, JolyBell.php, BananoviyRai.php**\
Эти PHP скрипты запускают **api_request.php** с особыми параметрами. Их запуск запланирован в cron.

**api_request.php**\
Этот PHP скрипт работает с API Вконтакте и фильтрует информацию из ответа\
Обязательные параметры:
* `--id` это id группы вконтакте или пользователь вконтакте, значение заменяет собой {id} в vk_api.txt (прим. `-88245281`)
* `--sourcespec` это любой термин который используется для идентификации разных источников (прим. `NaPriemeUShevcova`, `BananoviyRai`)
* `--deftitle` это заголовок поста по умолчанию, где _ заменяется на пробел (прим. `На_приеме_у_Шевцова`)
* `--sourcename` это название источника, где _ заменяется на пробел (исп. в флаерах, прим. `:i:_На_приеме_у_Шевцова`)
* `--sourceshort` это короткое название источника, где _ заменяется на пробел (исп. в флаерах, прим. `:i:Паблик`)

Необязательные параметры:
* `--flairid` это id флаера на реддите (прим. `2ea55bd8-e3e6-11ea-8a5c-0e7cceef0c57`)
* `--offset` это отступ количества постов, заменяет собой {offset} в vk_api.txt (прим. `2`)
* `--ignorecache` ставится, если вы хотите пропустить проверку дубликации поста (не имеет значений)
* `--skipdownload` ставится, если вы хотите пропустить загрузку видео с сервера ВК (не имеет значений)

**reddit_post.py**\
Скрипт Python, работающий с PRAW и публикующий новые посты. Параметры должны быть в том же порядке как и в api_request.php, но без имен (`--id`, `--deftitle` и т.д.). Если вы не хотите использовать флаер, поставьте `not-specified` вместо id.

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
  "subreddit": "Название сабреддита без r/",
  "is_moderator": true или false
}
```
если вы установите is_moderator в false, [reddit_post.py](/reddit_post.py) не станет добавлять флаер и тег спойлера, одобрять (approve) пост, писать к нему комментарий

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
