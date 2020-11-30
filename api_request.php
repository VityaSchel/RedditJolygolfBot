<?php

$longopts = array(
  "id:",
  "sourcespec:",
  "deftitle:",
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

$regular_source_settings = json_decode(file_get_contents(WORK_DIR."/configs/regular_source_settings.conf"));

$vk_api_response_raw = file_get_contents(file_get_contents(WORK_DIR."/secrets/vk_api.txt").$source_post_id);
$vk_api_response = json_decode($vk_api_response_raw, true);

if(!empty($vk_api_response['response']['items'][0]['is_pinned'])){
  $vk_api_response_raw = file_get_contents(file_get_contents(WORK_DIR."/secrets/vk_api.txt").$source_post_id."&offset=1");
  $vk_api_response = json_decode($vk_api_response_raw, true);
}

function contains($str, array $arr)
{
    foreach($arr as $a) {
        if (stripos($str,$a) !== false) return true;
    }
    return false;
}

function download_photo_from_vk($attached_photo, $iteration)
{
  global $options;
  global $post_data;

  $photo_variants = $attached_photo['photo']['sizes'];
  $post_image = end($photo_variants)['url'];
  $photo_iter = $iteration+1;
  file_put_contents(WORK_DIR.'/resources/picture/'.$options['sourcespec'].'_'.$photo_iter.'.jpg', file_get_contents($post_image));
  $post_data['images_count'] = $photo_iter;
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

  if($vk_post['marked_as_ads'] == "1"){
    die("Ads");
  }
  if(contains($vk_post['text'], $regular_source_settings->ads_words)){
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
    $post_data['title'] = str_replace("_", " ", $options['deftitle']);
  }
  $post_data['title'] = base64_encode($post_data['title']);

  $post_attachments = $vk_post['attachments'];
  if(empty($post_attachments)){
    $post_data['type'] = 'text';
  } else {
    $max_allowed_attachments = 5;
    $attachments_saved = 0;
    $post_data['images_count'] = 0;
    foreach($post_attachments as $attachment){
      if($attachments_saved >= $max_allowed_attachments){
        break;
      }
      if($attachments_saved == 0){
        switch($attachment['type']){
          case "photo":
            $post_data['type'] = "img";
            download_photo_from_vk($attachment, $attachments_saved);
            break;

          case "doc":
            if($attachment['doc']['type'] == 3) {
              // 3 = gif-document in vk api
              $post_data['type'] = "gif";
              $post_data['title'] .= "\n [".$regular_source_settings->gif_link_hint."](".$attachment['doc']['url'].")";
            } else {
              $post_data['type'] = "text";
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
            if($regular_source_settings->upload_videos_to_reddit) {
              $thumbnails_variants = $attachment['video']['image'];
              $thumbnail_url = end($thumbnails_variants)["url"];
              file_put_contents(WORK_DIR.'/resources/video/'.$options['sourcespec'].'_thumbnail.jpg', file_get_contents($thumbnail_url));

              if(array_key_exists('skipdownload', $options) != true){
                exec('youtube-dl https://vk.com/video'.$video_url.' -o '.WORK_DIR.'/resources/video/'.$options['sourcespec'].'_video.mp4 -f "bestvideo[height<='.$regular_source_settings->max_video_resolution.']+bestaudio/best[height<='.$regular_source_settings->max_video_resolution.']"');
              }
            }
            break;

          default:
            $post_data['type'] = "text";
            break;
        }
      } else {
        if($post_data['type'] == "img"){
          download_photo_from_vk($attachment, $attachments_saved);
        }
      }
      $attachments_saved += 1;
    }
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
  exec('python3 '.WORK_DIR.'/reddit_post.py '.$options['id'].' '.$options['sourcespec'].' '.$options['deftitle'].' '.$options['sourcename'].' '.$options['sourceshort'].' '.$flair_id);
}
?>
