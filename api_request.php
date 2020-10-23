<?php

// filepath syntax: work_dir/api_request.php --id -88245281 --sourcespec NaPriemeUShevcova --sourcename На_приеме_у_Шевцова --sourceshort Паблик
// options --flairid="{flair id}" and --ignorecache

$longopts = array(
  "id:",
  "sourcespec:",
  "sourcename:",
  "sourceshort:",
  "flairid::",
  "ignorecache"
);
$options = getopt(null, $longopts);

define('WORK_DIR', substr(file_get_contents(dirname(__FILE__)."/secrets/work_dir.txt"), 0, -1));
$source_post_id = $options['id'];

if(empty($options['id'])){
  die("Argument 'ID' is not defined");
}

$vk_api_response_raw = file_get_contents(file_get_contents(WORK_DIR."/secrets/vk_api.txt").$source_post_id);
$vk_api_response = json_decode($vk_api_response_raw, true);

if($vk_api_response['response']['items'][0]['is_pinned'] == 1){
  // post pinned, skip to newest after it
  $vk_api_response_raw = file_get_contents(file_get_contents(WORK_DIR."/secrets/vk_api.txt").$source_post_id."&offset=1");
  $vk_api_response = json_decode($vk_api_response_raw, true);
}

foreach($vk_api_response['response']['items'] as $vk_post){
  $post_id = $vk_post['id'];
  $last_submitted_id = file_get_contents(WORK_DIR."/".$options['sourcespec']."_last_posted_id.txt");

  // ignorecache is optional boolean you set when executing this script
  // it allows to skip checking for last posted id (use it for testing)
  if(array_key_exists('ignorecache', $options) != true){
    if($post_id == $last_submitted_id){
      die("Nothing to do");
    }
  }
  file_put_contents(WORK_DIR."/".$options['sourcespec']."_last_posted_id.txt", $post_id);

  if($vk_post['marked_as_ads'] == "1"){
    die("Ads");
  }
  if(!empty($vk_post['copy_history'])){
    if(count($vk_post['copy_history']) > 0){
      die("Repost");
    }
  }
  if(strpos($vk_post['text'],"WASD") > -1){
    die("Ads");
  }
  if(strpos($vk_post['text'],"wasd") > -1){
    die("Ads");
  }
  if(strpos($vk_post['text'], "youtu.be") > -1){
    die("Possible duplicate");
  }

  $submission_title = str_replace(";",",", $vk_post['text']);
  if($submission_title == ""){
    $submission_title = str_replace("_", " ", $options['sourcename']);
  }
  $post_attachments = $vk_post['attachments'];
  $submission_type = "";
  $post_image = "";
  if($post_attachments != ""){
    foreach($post_attachments as $attachment){
      switch($attachment['type']){
        case "photo":
          $submission_type = "img";
          $post_image = $attachment['photo']['sizes'][count($attachment['photo']['sizes'])-1]['url'];
          break;

        case "doc":
          if($attachment['doc']['type'] == 3) {
            // weird vk api; 3 means gif-document
            $submission_type = "gif";
            $submission_title .= "\n [Нажмите сюда, чтобы увидеть прикрепеленный к оригиналу GIF](".$atch['doc']['url'].")";
          } else {
            $submission_type = "text";
          }
          break;

        case "poll":
          $submission_type = 'poll:'.str_replace("#", "", $attachment['poll']['answers'][0]['text']);
          for($j = 1; $j < count($attachment['poll']['answers']); $j++){
            $submission_type .= "#".str_replace("#", "", $attachment['poll']['answers'][$j]['text']);
          }
          break;

        case "video":
          $submission_type = 'video:'.$attachment['video']['owner_id']."_".$attachment['video']['id'];
          break;
      }
    }
  } else {
    // unsupported type
    $submission_type = 'text';
  }

  $post_likes = $vk_post['likes']['count'];
  $post_reposts = $vk_post['reposts']['count'];
  $post_comments = $vk_post['comments']['count'];
  $post_views = $vk_post['views']['count'];
  $post_url = $vk_post['from_id']."_".$vk_post['id'];

  file_put_contents(WORK_DIR."/resources/data/".$options['sourcespec'].".txt", $submission_type.';'.$post_image.';'.$post_likes.';'.$post_reposts.';'.$post_comments.';'.$post_views.';'.base64_encode($submission_title).';'.$post_url);
  if($submission_type == "img"){
    file_put_contents(WORK_DIR.'/resources/picture/'.$options['sourcespec'].'.jpg', file_get_contents($post_image));
  }
  if(strlen($options["flairid"]) < 1){
    $flair_id = "not-specified";
  } else {
    $flair_id = $options['flairid'];
  }
  file_put_contents(WORK_DIR."/logs"."/".$options['sourcespec']."_python.txt", shell_exec('python3 '.WORK_DIR.'/reddit_post.py '.$options['sourcespec'].' '.$options['sourcename'].' '.$options['sourceshort'].' '.$flair_id).PHP_EOL, FILE_APPEND);
}
?>
