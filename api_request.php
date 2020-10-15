<?php

// filepath syntax: work_dir/api_request.php -88245281 NaPriemeUShevcova На_приеме_у_Шевцова Паблик

define('WORK_DIR', file_get_contents(dirname(__FILE__)."/secrets/work_dir.txt"));
$sourceID = $argv[1];

if(empty($argv[1])){die("Argument 1 incorrect");}

$resp = file_get_contents(file_get_contents(WORK_DIR."secrets/vk_api.txt").$sourceID);
$resp = json_decode($resp, true);

if($resp['response']['items'][0]['is_pinned'] == 1){
  // post pinned, skip to newest after it
  $resp = file_get_contents(file_get_contents(WORK_DIR."secrets/vk_api.txt").$sourceID."&offset=1");
  $resp = json_decode($resp, true);
}

foreach($resp['response']['items'] as $item){
  $id = $item['id'];
  $idlast = file_get_contents(WORK_DIR.$argv[2]."_last_posted_id.txt");
  if($id == $idlast){
    die("Nothing to do");
  }
  file_put_contents(WORK_DIR.$argv[2]."_last_posted_id.txt", $id);

  if($item['marked_as_ads'] == "1"){
    die("Ads");
  }
  if(count($item['copy_history']) > 0){
    die("Repost");
  }
  if(strpos($item['text'],"WASD") > -1){
    die("Ads");
  }
  if(strpos($item['text'],"wasd") > -1){
    die("Ads");
  }
  if(strpos($item['text'],"youtu.be") > -1){
    die("Possible duplicate");
  }
  $title = str_replace(";",",",$item['text']);
  if($title == ""){
    $title = str_replace("_", " ",$argv[3]);
  }
  $attachs = $item['attachments'];
  $type = "";
  if($attachs != ""){
    foreach($attachs as $atch){
      switch($atch['type']){
        case 'photo':
          $image = $atch['photo']['sizes'][count($atch['photo']['sizes'])-1]['url'];
          $type = 'img';
          break;

        case 'doc':
          $title .= "\n [Нажмите сюда, чтобы увидеть прикрепеленный к оригиналу GIF](".$atch['doc']['url'].")";
          $type = 'text';
          break;

        case "poll":
          $type = 'poll:'.str_replace("#", "", $atch['poll']['answers'][0]['text']);
          for($j = 1; $j < count($atch['poll']['answers']); $j++){
            $type .= "#".str_replace("#", "", $atch['poll']['answers'][$j]['text']);
          }
          break;
      }
    }
  } else {
    $type = 'text';
  }
  $likes = $item['likes']['count'];
  $reposts = $item['reposts']['count'];
  $comments = $item['comments']['count'];
  $views = $item['views']['count'];
  $lin = $item['from_id']."_".$item['id'];
  file_put_contents(WORK_DIR."resources/data/".$argv[2].".txt", $type.';'.$image.';'.$likes.';'.$reposts.';'.$comments.';'.$views.';'.base64_encode($title).';'.$lin);
  if($type == 'img'){
    $url = $image;
    file_put_contents(WORK_DIR.'resources/picture/'.$argv[2].'.jpg', file_get_contents($url));
  }
  file_put_contents(WORK_DIR."logs/".$argv[2]."_python.txt", shell_exec('python3 '.WORK_DIR.'reddit_post.py '.$argv[2].' '.$argv[3].' '.$argv[4]).PHP_EOL, FILE_APPEND);
}
?>
