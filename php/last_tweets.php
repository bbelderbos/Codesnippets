<?php
$user = 'bbelderbos';
$numTweets = 10; 

$json = file_get_contents("http://twitter.com/status/user_timeline/$user.json?count=$numTweets"); 
if($json === FALSE) exit;
$latestTweets = json_decode($json, true); //getting the file content as array
 
//echo "<pre>";print_r($latestTweets);echo "</pre>";exit; // debug 
?>
<div style="font-size: 75%; width: 200px;">

<?php 
foreach($latestTweets as $tweet) {
	$tweetText = $tweet['text'];
	
	// URLs (from http://www.phpro.org/examples/URL-to-Link.html)
	$tweetText = preg_replace("/([\w]+:\/\/[\w-?&;#~=\.\/\@]+[\w\/])/i","<a target=\"_blank\" href=\"$1\" target=\"_blank\">$1</a>",$tweetText);
	
	// twitter handles
	$tweetText = preg_replace('/(@\S+)/i',"<a target=\"_blank\" href=\"http://twitter.com/$1\" target=\"_blank\">$1</a>",$tweetText);
	
	// hash tags map to search?q=#hash
	$tweetText = preg_replace('/(#)(\S+)/i',"<a target=\"_blank\" href=\"http://twitter.com/search?q=%23$2\" target=\"_blank\">$1$2</a>",$tweetText);	
	
	echo '<img width="20px" src="'.$tweet['user']['profile_image_url'].'" alt="bob avatar"><p style="display:inline; position: relative; bottom: 4px; left: 5px;">'.$tweetText . "</p><br>";
	
}
?>