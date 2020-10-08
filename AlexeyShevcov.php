<?php

define('WORK_DIR', file_get_contents("./secrets/work_dir.txt"));
$resp = file_get_contents(file_get_contents("./secrets/vk_api.txt")."34347140");
$resp = json_decode($resp, true);

foreach($resp['response']['items'] as $item){
  $id = $item['id'];
  $idlast = file_get_contents("AlexeyShevcov_last_posted_id.txt");
  if($id == $idlast){
    die("Nothing to do");
  }
  file_put_contents("AlexeyShevcov_last_posted_id.txt", $id);

  if(count($item['copy_history']) > 0){
    die("Repost");
  }
  if(strpos($item['text'],"WASD") > -1){
    die("Ads");
  }
  if(strpos($item['text'],"wasd") > -1){
    die("Ads");
  }
  $title = str_replace(";",",",$item['text']);
  if($title == ""){
    $title = "Алексей Шевцов";
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
  file_put_contents("./resources/data/AlexeyShevcov.txt", $type.';'.$image.';'.$likes.';'.$reposts.';'.$comments.';'.$views.';'.base64_encode($title).';'.$lin);
  if($type == 'img'){
    $url = $image;
    file_put_contents('./resources/picture/AlexeyShevcov.jpg', file_get_contents($url));
  }
  file_put_contents("./logs/AlexeyShevcov_python.txt", shell_exec('python3 '.WORK_DIR.'AlexeyShevcov.py').PHP_EOL, FILE_APPEND);
}
?>
