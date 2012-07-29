#!/usr/bin/php
<?php
date_default_timezone_set('Europe/Madrid'); 
$url = "http://www.lasexta.com/guiatv/ver/lasexta3"; 
$sexta = useCurl($url);
$lines = explode("\n", $sexta);

foreach($lines as $line) {
  if(strstr($line, ".pdf")) {
    $pdf = preg_replace('/.*<a href="(.*?)" .*/', "$1", $line);
    $email = "EMAIL";
    $subject = "Pelis Sexta Todo Cine dia $date";
    mail($email, $subject, $pdf);
    break; 
  } 
}


function useCurl($url) {
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_HEADER, 0);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  curl_setopt($ch, CURLOPT_FAILONERROR, 1);

  $results = curl_exec($ch);
  $headers = curl_getinfo($ch);
  
  if($headers['http_code'] != 200) {
    die("Curl could not get info / error no: ".curl_errno($ch).", error msg: ".curl_error($ch) . "\n" );
  }  

  curl_close($ch);
  return $results;
}
?>
