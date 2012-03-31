<?php
// from the PHP-SDK <http://github.com/facebook/php-sdk/blob/master/examples/example.php>
require 'fbsdk/src/facebook.php';
$facebook = new Facebook(array(
  'appId'  => '<your app id>',
  'secret' => '<your app secret>',
));

$user = $facebook->getUser();

if ($user && $_POST) {
  try {
	$page_to = (isset($_POST['page_to']))? $_POST['page_to'] : '';
	$message = (isset($_POST['message']))? $_POST['message'] : '';
	$link = (isset($_POST['link']))? $_POST['link'] : '';
	
	echo "Posting to <a target='_blank' href='http://facebook.com/$page_to'>$page_to</a> ...<br>"; 
	
	$page_info = $facebook->api("/$page_to?fields=access_token");
	if( !empty($page_info['access_token']) ) {
		$args = array(
			'access_token'  => $page_info['access_token'],
			'message'       => $message,
			'link'			=> $link,
			'method'       => 'post'
		);
		if($post_id = $facebook->api("/$page_to/feed","post",$args)){
			echo "Status: OK: posted to $page_to<br>FB API response: <br>"; 
			print_r($post_id);
			echo '<br><a href="page.php">New post</a>';
		} else {
			echo "Status: Error: could not post to FB page";
		}
	}
  } catch (FacebookApiException $e) {
    error_log($e);
    $user = null;
  }
}

// Login or logout url will be needed depending on current user state.
if ($user) {
  $logoutUrl = $facebook->getLogoutUrl();
} else {
  $loginUrl = $facebook->getLoginUrl(array('scope'=>'manage_pages,publish_stream'));
}
?>
<!doctype html>
<html xmlns:fb="http://www.facebook.com/2008/fbml">
  <head>
    <title>Post to FB page</title>
    <link rel="stylesheet" href="style.css" type="text/css" media="screen" charset="utf-8" />
  </head>
  <body>
    <h1>Post to FB page</h1>

    <?php if ($user): ?>
      <div id="links" style="position: absolute; top: 5px; right: 10px;">
		<a href="<?php echo $logoutUrl; ?>">Logout</a> | <a href="page.php">Start over</a>
	  </div>
	  
	  <form method="post" id="sendMessage">
		<label>Page: </label><br>
		<select name="page_to">
			<?php
			$result = $facebook->api("/me/accounts");
			foreach($result["data"] as $page) { 
				if($page["category"] == "Application") {
					continue; // app pages dont work for this exercise
				}
				echo '<option value="'.$page["id"].'" ';
				if ($page["id"] == $page_to) {
					echo ' selected="selected"';
				}
				echo '>'. $page["name"] . '</option>' ;
			}   
			?>
		</select><br>
		<label>URL: </label><br>
		<input type="text" name="link" value="<?php echo $link; ?>"><br>
		<label>Message: </label><br>
		<textarea name="message" cols="50" rows="20"><?php echo $message; ?></textarea><br>
		<input class="submit" type="submit" value="Post!">
  	  </form>
    <?php else: ?>
      <div>
        <a href="<?php echo $loginUrl; ?>">Login with Facebook</a>
      </div>
    <?php endif ?>

    <pre><?php // print_r($_SESSION); ?></pre>

  </body>
</html>

