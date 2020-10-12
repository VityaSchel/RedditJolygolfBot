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
Директория для логов\
*Игнорируется, ничего не помещайте здесь*

### resources (директория)
Информация для сообщения между скриптами **api_request.php** и **reddit_post.py**\
*Ничего не помещайте здесь*

#### resources/data
**NaPriemeUShevcova.txt, AlexeyShevcov.txt, ItpediaYoutube.txt, JolyBell.txt, BananoviyRai.txt**\
Формат любого из файлов:\
`{тип(text,poll:..#..,img)};{ссылка на изображение на серверах вк};{кол-во лайков};{кол-во репостов};{кол-во комментариев};{кол-во просмотров};{заголовок или текст поста в UTF-8 в base64};{id в вк groupid_postid}`\
*TODO: Использовать JSON*\
*Игнорируется, ничего не помещайте здесь*

#### resources/picture
**NaPriemeUShevcova.jpg, AlexeyShevcov.jpg, ItpediaYoutube.jpg, JolyBell.jpg, BananoviyRai.jpg**\
Изображения в максимальном качестве, скачанные скриптом **api_request.php** с сервера ВК и позже загруженные на сервер reddit с помощью PRAW\
*Игнорируется, ничего не помещайте здесь*

### secrets (директория)
Для приватной информации: пароли, ключи api, рабочая директория\
*Игнорируется, ничего не помещайте здесь*
