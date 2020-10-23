<?php

// filepath syntax: work_dir/youtube_api.php UU6bTF68IAV1okfRfwXIP1Cg{this is playlist id} ItpediaYoutube itpedia

define('WORK_DIR', substr(file_get_contents(dirname(__FILE__)."/secrets/work_dir.txt"), 0, -1));
$source_spec = $argv[2];

$youtube_api_response = file_get_contents(file_get_contents(WORK_DIR."/secrets/youtube_api.txt".$argv[1]));
$youtube_api = json_decode($youtube_api_response, true);

$snippet_data = $youtube_api['items'][0]['snippet'];
$video_id = $snippet_data['resourceId']['videoId'];
$last_submitted_id = file_get_contents(WORK_DIR."/".$source_spec."_last_posted_id.txt");
if($video_id == $last_submitted_id){
  die("Nothing to do");
}
$video_name = $snippet_data['title'];

$video_url = "https://www.youtube.com/watch?v=".$video_id;
file_put_contents(WORK_DIR."/resources/data/".$source_spec.".txt", $video_url.';'.$video_name);
shell_exec('python3 '.WORK_DIR.'/reddit_youtube_video_post.py '.$source_spec.' '.$argv[3]);
file_put_contents(WORK_DIR."/".$source_spec."_last_posted_id.txt", $video_id);

?>
