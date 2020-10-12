<?php

// filepath syntax: work_dir/youtube_api.php UU6bTF68IAV1okfRfwXIP1Cg{this is playlist id} ItpediaYoutube itpedia

define('WORK_DIR', file_get_contents(dirname(__FILE__)."/secrets/work_dir.txt"));
$source = $argv[2];

$youtubeapiresp = file_get_contents(file_get_contents(WORK_DIR."secrets/youtube_api.txt".$argv[1]));
$youtubeapi = json_decode($youtubeapiresp, true);

$snippet = $youtubeapi['items'][0]['snippet'];

$title = $snippet['title'];
$id = $snippet['resourceId']['videoId'];
$lastid = file_get_contents($source."_last_posted_id.txt");
if($id == $lastid){
  die("Nothing to do");
}
$link = "https://www.youtube.com/watch?v=".$id;
file_put_contents(WORK_DIR."resources/data/".$source.".txt", $link.';'.$title);
shell_exec('python3 '.WORK_DIR.'reddit_youtube_video_post.py '.$argv[2].' '.$argv[3]);
file_put_contents($source."_last_posted_id.txt", $id);

?>
