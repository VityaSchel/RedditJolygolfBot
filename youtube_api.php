<?php

// filepath syntax: work_dir/youtube_api.php --playlistID UU6bTF68IAV1okfRfwXIP1Cg --sourcespec ItpediaYoutube --sourcename itpedia
// optional --flairid "6a360654-26d9-11ea-b36f-0ee735f1b64b" --ignorecache

$longopts = array(
  "playlistID:",
  "sourcespec:",
  "sourcename:",
  "flairid::",
  "ignorecache"
);
$options = getopt(null, $longopts);
define('WORK_DIR', substr(file_get_contents(dirname(__FILE__)."/secrets/work_dir.txt"), 0, -1));

if(empty($options['sourcespec'])){
  die("Argument sourcespec is not defined");
}
$source_spec = $options['sourcespec'];

if(empty($options['playlistID'])){
  die("Argument playlistID is not defined");
}
$playlistID = $options['playlistID'];

$youtube_api_response = file_get_contents(file_get_contents(WORK_DIR."/secrets/youtube_api.txt").$playlistID);
$youtube_api = json_decode($youtube_api_response, true);

$snippet_data = $youtube_api['items'][0]['snippet'];
$video_id = $snippet_data['resourceId']['videoId'];
$last_submitted_id = file_get_contents(WORK_DIR."/".$source_spec."_last_posted_id.txt");
if(array_key_exists('ignorecache', $options) != true){
  if($video_id == $last_submitted_id){
    die("Nothing to do");
  }
}
file_put_contents(WORK_DIR."/".$source_spec."_last_posted_id.txt", $video_id);
$video_name = $snippet_data['title'];
$flair_id = "";
if(strlen($options["flairid"]) < 1){
  $flair_id = "not-specified";
} else {
  $flair_id = $options["flairid"];
}
$video_url = "https://www.youtube.com/watch?v=".$video_id;
file_put_contents(WORK_DIR."/resources/data/".$source_spec.".txt", $video_url.';'.$video_name);
exec('python3 '.WORK_DIR.'/reddit_youtube_video_post.py '.$source_spec.' '.$options['sourcename'].' '.$flair_id);


?>
