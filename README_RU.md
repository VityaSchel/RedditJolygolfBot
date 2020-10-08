# RedditJolygolfBot
Бот для сабреддита [r/Jolygolf](https://www.reddit.com/r/Jolygolf/) о видеоблоггере Алексее Шевцове. Умеет постить изображения, опросы, ссылки из разных источников как VK и YouTube

## Краткий обзор
### Корневые файлы
**NaPriemeUShevcova.php, AlexeyShevcov.php, JolyBell.php**
PHP скрипты, работающие с API Вконтакте и фильтрующие информацию

**NaPriemeUShevcova.py, AlexeyShevcov.py, JolyBell.py**
Скрипты Python, работающие с PRAW и публикующие новые посты

**ItpediaYoutube.php**
Этот скрипт обращается к YouTube API, чтобы проверить новые видео на [Канале Itpedia](https://www.youtube.com/user/itpediachannel)

**ItpediaYoutube.py**
Этот скрипт постит ссылки на новые видео в сабреддит

**AlexeyShevcov_last_posted_id.txt, NaPriemeUShevcova_last_posted_id.txt, ItpediaYoutube_last_posted_id.txt, JolyBell_last_posted_id.txt**
Файлы для сравнения текущего последнего ID от API и того, что в кеше (последний пост). Используется скриптами \*.php

### logs (директория)
Директория для логов\
*Игнорируется, ничего не помещайте здесь*

### resources (директория)
Информация для сообщения между скриптами \*.php и \*.py\
*Ничего не помещайте здесь*

#### resources/data
**NaPriemeUShevcova.txt, AlexeyShevcov.txt, ItpediaYoutube.txt, JolyBell.txt**
Data format:\
`{тип(text,poll:..#..,img)};{ссылка на изображение на серверах вк};{кол-во лайков};{кол-во репостов};{кол-во комментариев};{кол-во просмотров};{заголовок или текст поста в UTF-8 в base64};{id в вк groupid_postid}`\
*TODO: Использовать JSON*\
*Игнорируется, ничего не помещайте здесь*

#### resources/picture
**NaPriemeUShevcova.jpg, AlexeyShevcov.jpg, ItpediaYoutube.jpg, JolyBell.jpg**
Изображения в максимальном качестве, скачанные \*.php скриптом с сервера ВК и позже загруженные на сервер reddit с помощью PRAW\
*Игнорируется, ничего не помещайте здесь*

### secrets (директория)
Для приватной информации: пароли, ключи api, рабочая директория\
*Игнорируется, ничего не помещайте здесь*
