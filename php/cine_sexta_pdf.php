<?php
date_default_timezone_set('Europe/Madrid'); 

$url = "http://www.lasexta.com/guiatv/ver/lasexta3"; 
$sexta = useCurl($url);
$lines = explode("\n", $sexta);

foreach($lines as $line) {
	if(strstr($line, ".pdf")) {
		$pdf = preg_replace('/.*<a href="(.*?)" .*/', "$1", $line);
		echo "Downloading $pdf ...\n";
    $pdf_file = basename($pdf);
		useCurl($pdf, $pdf_file);
		break; 
	} 
}

if(is_file($pdf_file)) {
  $date = date("m.d.Y");
  $email = "YOUR EMAIL ADDRESS";
  $subject = "Pelis Sexta Todo Cine dia $date";
  $cmd = "uuencode $pdf_file $pdf_file | mailx -s $subject $email";
  exec($cmd, $output); 
  if($output) {
    echo "Output mailCmd: ";
    print_r($output, true);
    echo "\n";
  }
} else {
  die("File $pdf_file not found.\n");
}


function useCurl($url, $file=FALSE) {
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);

  if($file) {
  	$fp = fopen($file, 'w');
    curl_setopt($ch, CURLOPT_FILE, $fp);
  } else {
  	curl_setopt($ch, CURLOPT_HEADER, 0);
  	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
  	curl_setopt($ch, CURLOPT_FAILONERROR, 1);
  }
  
  $results = curl_exec($ch);
  $headers = curl_getinfo($ch);
  
  if($headers['http_code'] != 200) {
  	die("Curl could not get info / error no: ".curl_errno($ch).", error msg: ".curl_error($ch) . "\n" );
  }  

  curl_close($ch);
  
  if($file) fclose($fp);

  return $results;
}
?>
