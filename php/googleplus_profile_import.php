<html>
<head>
	<title>Google+ importer</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<meta name="description" content="This page imports your google+ profile" />
</head>
<body>
<?php
// thanks!! to: 
// -> http://point7.wordpress.com/2011/07/10/rudimentary-googleplus-api/ 

// more php https://github.com/jmstriegel/php.googleplusapi

$user = $_GET['u'];

$query = "http://my.syyn.cc/gpapi?id={$user}&type=profile";

$out = file_get_contents($query);
$response = json_decode($out, true);

$g = array();
$g['usr'] = ($response[2])? $response[2]: '';
$g['avatar'] = ($response[3])? $response[3].'?sz=90': '';
$g['name'] = ($response[4][3])? $response[4][3]: '';
$g['title'] = ($response[6][1])? $response[6][1]: '';
$g['location'] = ($response[9][1])? $response[9][1]: '';

echo '<h1><a href="'.$g['usr'].'">'.$g['name'].'</a></h1>';

echo '<h2>Personal Data</h2>
	<ul>
		<li>Avatar: <img src="'.$g['avatar'].'"></li>
		<li>Title: ' .$g['title'] . '</li>
		<li>Location: ' .$g['location'] . '</li>		
 	</ul>';


if(!empty($response[14][1])) {
	echo '<h2>About me</h2>
			<p>'.$response[14][1].'</p>';
}

if(!empty($response[7][1])) {
	echo '<h2>Work</h2>
	<table><th>Company</th><th>Function</th>';
	foreach($response[7][1] as $r) {
		echo '<tr>';
		echo '<td>'.$r[0].'</td>';
		echo '<td>'.$r[1].'</td>';
		echo '</tr>';
	}
	echo '</table>';	
}

if(!empty($response[8][1])) {
	echo '<h2>Education</h2>
	<table><th>Institute</th><th>Studies</th>';
	foreach($response[8][1] as $r) {
		echo '<tr>';
		echo '<td>'.$r[0].'</td>';
		echo '<td>'.$r[1].'</td>';
		echo '</tr>';
	}
	echo '</table>';	
}


if(!empty($response[11][0])) {
	echo '<h2>Links</h2>
	<table><th>Name</th><th>URL</th>';
	foreach($response[11][0] as $r) {
		echo '<tr>';
		echo '<td>'.$r[3].'</td>';
		echo '<td><a href="'.$r[1].'" target="_blank" 
			style="padding-left: 20px; background:url(\'http:'.$r[2].'\') top left
			no-repeat">'.$r[1].'</a></td>';
		echo '</tr>';
	}
	echo '</table>';	
}
?>
</body>
</html>

