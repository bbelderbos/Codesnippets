<?php 
# thanks to http://phat-reaction.com/googlefonts.php
$fontsSeraliazed = file_get_contents('http://phat-reaction.com/googlefonts.php?format=php');
$fontArray = unserialize($fontsSeraliazed);
#print_r($fontArray);
?>
