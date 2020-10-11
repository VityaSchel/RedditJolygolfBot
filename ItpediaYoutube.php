<?php

define('WORK_DIR', file_get_contents(dirname(__FILE__)."/secrets/work_dir.txt"));
$jj = file_get_contents(file_get_contents(WORK_DIR."secrets/youtube_api.txt"));
$a = json_decode($jj, true);

$aa = $a['items'][0]['snippet'];

$title = $aa['title'];
$id = $aa['resourceId']['videoId'];
$lastid = file_get_contents("ItpediaYoutube_last_posted_id.txt");
if($id == $lastid){
  die("Nothing to do");
}
$link = "https://www.youtube.com/watch?v=".$id;
file_put_contents(WORK_DIR."resources/data/ItpediaYoutube.txt", $link.';'.$title);
shell_exec('python3 '.WORK_DIR.'ItpediaYoutube.py');
file_put_contents("ItpediaYoutube_last_posted_id.txt", $id);

?>
