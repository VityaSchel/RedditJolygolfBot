<?php

// filepath syntax: work_dir/api_request.php --id -88245281 --sourcespec NaPriemeUShevcova --sourcename На_приеме_у_Шевцова --sourceshort Паблик
// options --flairid="{flair id}", --skipdownload --ignorecache

$longopts = array(
  "id:",
  "sourcespec:",
  "sourcename:",
  "sourceshort:",
  "flairid::",
  "ignorecache",
  "skipdownload",
);
$options = getopt(null, $longopts);
$post_data = array();

define('WORK_DIR', substr(file_get_contents(dirname(__FILE__)."/secrets/work_dir.txt"), 0, -1));
$source_post_id = $options['id'];

if(empty($options['id'])){
  die("Argument 'ID' is not defined");
}

$vk_api_response_raw = file_get_contents(file_get_contents(WORK_DIR."/secrets/vk_api.txt").$source_post_id);
$vk_api_response = json_decode($vk_api_response_raw, true);

if(!empty($vk_api_response['response']['items'][0]['is_pinned'])){
  // post pinned, skip to newest after it
  $vk_api_response_raw = file_get_contents(file_get_contents(WORK_DIR."/secrets/vk_api.txt").$source_post_id."&offset=1");
  $vk_api_response = json_decode($vk_api_response_raw, true);
}

foreach($vk_api_response['response']['items'] as $vk_post){
  $post_id = $vk_post['id'];
  $last_submitted_id = file_get_contents(WORK_DIR."/".$options['sourcespec']."_last_posted_id.txt");

  if(array_key_exists('ignorecache', $options) != true){
    if($post_id == $last_submitted_id){
      die("Nothing to do");
    }
  }
  file_put_contents(WORK_DIR."/".$options['sourcespec']."_last_posted_id.txt", $post_id);
  // ignorecache is optional boolean you set when executing this script
  // it allows to skip checking for last posted id (use it for testing)

  if($vk_post['marked_as_ads'] == "1"){
    die("Ads");
  }
  if(strpos($vk_post['text'],"WASD") !== FALSE || strpos($vk_post['text'],"wasd") !== FALSE){
    die("Ads");
  }
  if(!empty($vk_post['copy_history'])){
    if(count($vk_post['copy_history']) > 0){
      die("Repost");
    }
  }
  if(strpos($vk_post['text'], "youtu.be") !== FALSE){
    die("Possible duplicate");
  }

  $post_data['title'] = str_replace(";",",", $vk_post['text']);
  if($post_data['title'] == ""){
    $post_data['title'] = str_replace("_", " ", $options['sourcename']);
  }
  $post_data['title'] = base64_encode($post_data['title']);

  $post_attachments = $vk_post['attachments'];
  $post_image = "";
  if($post_attachments != ""){
    foreach($post_attachments as $attachment){
      switch($attachment['type']){
        case "photo":
          $post_data['type'] = "img";
          $photo_variants = $attachment['photo']['sizes'];
          $post_image = end($photo_variants)['url'];
          file_put_contents(WORK_DIR.'/resources/picture/'.$options['sourcespec'].'.jpg', file_get_contents($post_image));
          // downloading photo
          break;

        case "doc":
          if($attachment['doc']['type'] == 3) {
            // weird vk api; 3 means gif-document
            $post_data['type'] = "gif";
            $post_data['title'] .= "\n [Нажмите сюда, чтобы увидеть прикрепеленный к оригиналу GIF](".$atch['doc']['url'].")";
          } else {
            $post_data['type'] = "text";
            //unsupported document
          }
          break;

        case "poll":
          $poll_answers = $attachment['poll']['answers'];
          $post_data['type'] = "poll";
          $poll_data = array();
          for($j = 0; $j < count($poll_answers); $j++){
            array_push($poll_data, str_replace("#", "", $poll_answers[$j]['text']));
          }
          $post_data['poll_data'] = $poll_data;
          break;

        case "video":
          $post_data['type'] = "video";
          $video_url = $attachment['video']['owner_id']."_".$attachment['video']['id'];
          $post_data['video_data'] = $video_url;
          $thumbnails_variants = $attachment['video']['image'];
          $thumbnail_url = end($thumbnails_variants)["url"];
          file_put_contents(WORK_DIR.'/resources/video/'.$options['sourcespec'].'_thumbnail.jpg', file_get_contents($thumbnail_url));
          // downloading thumbnail
          if(array_key_exists('skipdownload', $options) != true){
            exec('youtube-dl https://vk.com/video'.$video_url.' -o '.WORK_DIR.'/resources/video/'.$options['sourcespec'].'_video.mp4 -f "bestvideo[height<=360]+bestaudio/best[height<=360]"');
            // downloading video
          }
          // skipdownload is optional boolean you set when executing this script
          // it allows to skip downloading the video
          // cause it takes 5-10 seconds for really short video
          break;

        default:
          $post_data['type'] = "text";
          // unsupported type
          break;
      }
    }
  } else {
    $post_data['type'] = 'text';
  }

  $post_data['likes_count'] = $vk_post['likes']['count'];
  $post_data['reposts_count'] = $vk_post['reposts']['count'];
  $post_data['comments_count'] = $vk_post['comments']['count'];
  $post_data['views_count'] = $vk_post['views']['count'];
  $post_data['post_id'] = $vk_post['from_id']."_".$vk_post['id'];

  file_put_contents(WORK_DIR."/resources/data/".$options['sourcespec'].".txt", json_encode($post_data));
  if(strlen($options["flairid"]) < 1){
    $flair_id = "not-specified";
  } else {
    $flair_id = $options['flairid'];
  }
  exec('python3 '.WORK_DIR.'/reddit_post.py '.$options['sourcespec'].' '.$options['sourcename'].' '.$options['sourceshort'].' '.$flair_id);
}
?>
