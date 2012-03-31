<?php
//copyright (c) 2011 bob belderbos
//created: January 2011 
//post: http://bobbelderbos.com/2011/01/build-movie-trailer-api-using-gdata/

if(!$_GET['q']) {
    echo "no movie title given"; 
    exit; 
}
$q = $_GET['q'];

$q = preg_replace("/\([0-9].*\)/", "",$q);  

$toReplace = array("'"," ");
$replWith = array("+","+");
$q = str_replace($toReplace, $replWith,$q);
//$q .= 'trailer';
$q .= '+trailer';

$feedURL = 'http://gdata.youtube.com/feeds/api/videos?q='.$q.'&start-index=1&max-results=1';

// read feed into SimpleXML object
$sxml = simplexml_load_file($feedURL);

/*echo '<pre>';
print_r($sxml);
echo '</pre>';
exit; */

// iterate over entries in feed
foreach ($sxml->entry as $entry) {
  // get nodes in media: namespace for media information
  $media = $entry->children('http://search.yahoo.com/mrss/');
  // get video player URL
  $attrs = $media->group->player->attributes();
  $trailer = $attrs['url']; 
}

$trailer = str_replace('watch?v=','v/',$trailer);
?>
<object width="640" height="385"><param name="movie" value="<?php echo $trailer ;?>?fs=1&amp;hl=en_US"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="<?php echo $trailer ;?>?fs=1&amp;hl=en_US" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="640" height="385"></embed></object>
