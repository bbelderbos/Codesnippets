<?php
$yql = "select * from twitter.search where q='xyz'";  
$query = "http://query.yahooapis.com/v1/public/yql?q=";
$query .= urlencode($yql);
$query .= "&format=json&env=store://datatables.org/alltableswithkeys";
$info = file_get_contents($query, true);
$info = json_decode($info); // echo "<pre>"; print_r($info ); echo "</pre>"; exit; 

foreach($info->query->results->results as $item) { 
  // query->results->results might differ
  //process results
}
?>
