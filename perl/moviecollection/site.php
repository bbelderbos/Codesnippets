<!doctype html>
<head>
  <meta charset="ISO-8859-1">
  <title>movie collection</title>

  <meta name="description" content="movie collection">
  <meta name="author" content="bob belderbos">

  <style>
	body {width: 960px; background: #333; margin: 0 auto; font-size: small; font-family: verdana, sans-serif; }
	ul {background-color: #666; padding: 9px; overflow: hidden; 
		border-right: 1px solid #fff; border-bottom: 2px solid #fff; }
	li {float: left; width: 280px; list-style: none; background-color: #fff;
		margin: 5px; padding: 9px; border-right: 1px solid #000; border-bottom: 2px solid #333;  }
	li.clear {clear: both;}
	img {width: 100px; padding-top: 5px; margin-top: 10px; }
	a {color: #900; text-decoration: none; }
	h1 {font-size: 1.5em; margin-left: 20px; color: white; }
	h2 {font-size: 1.2em; height: 40px; background-color: #ccc; padding: 5px;}
	h3 {font-size: 1em;}
	div {border-top: 1px solid #ccc; padding: 0 5px; }
	div.genreWrapper { border-bottom: 2px solid #ccc; font-size: 90%; background-color:#eee; }
	div.poster {height: 150px; width: 100px; float: right; }
	div.castWrapper {width: 150px; float: left; height: 220px; }
	div.plotWrapper {clear: both;  height: 150px; font-size: 85%;}
	div.specWrapper {clear: both;  height: 40px; font-size: 90%; background-color:#ddd; }
  </style>

</head>

<body>
	<ul>
		<?php
		$db_conn = new mysqli('localhost', 'user', 'password', 'database');
		$subtitle = '';
		
		if($_GET) {
			$col = $_GET['c']; # in real life, you need to secure this
			$filter = strtolower($_GET['q']);  # iidem, this example is just localhost / private use
			$q = "SELECT * FROM table where lcase($col) like '%$filter%' order by title";
			$subtitle = '<br><small> for /'.$col.'/ = %'.$filter.'%  -- <a style="color: #ccc; " href="index.php">view all</a> --</small>';
		} else {
			$q = "SELECT * FROM table order by title";			
		}
		$r = $db_conn->query($q);
		$numMovies = mysqli_num_rows($r);
		echo '<h1>'.$numMovies . ' titles in Movie Collection' . $subtitle . '</h1>';
		
		if(mysqli_num_rows($r)) { 
			$counter = 0;
			
			while($row = $r ->fetch_object()){
				 				
				if($counter % 3 == 0) {
					echo '<li class="clear">';
				} else {
					echo '<li>';
				}
				echo '<h2>'.$row->title.'<small>(<a href="index.php?c=year&q='.$row->year.'">'.$row->year.'</a>)</small></h2>';
				
				echo '<div class="genreWrapper"><p>';
				
				$genres = explode(', ',$row->genre);
				$genresOut = '';
				foreach ($genres as $g) {
					$genresOut .= '<a href="index.php?c=genre&q='.$g.'">'.$g.'</a>, ';
				}
				echo substr($genresOut, 0, -2);
				
				echo '<br>Rated: '.$row->rating.'</p>';
				echo '</div>';
				
				echo '<div class="poster">';
				if($row->poster == "N/A"){
					echo '<img src="http://entertainment.ie/movie_trailers/trailers/flash/posterPlaceholder.jpg">'; 
				} else {
					echo '<img src="'.$row->poster.'">';
				}
				echo '</div>';
	
				echo '<div class="castWrapper">';
				echo '<h3>Cast</h3>';
				echo '<p>Director: ';
				
				$directors = explode(', ',$row->director);
				$directorsOut = '';
				foreach ($directors as $d) {
					$directorsOut .= '<a href="index.php?c=director&q='.$d.'">'.$d.'</a>, ';
				}
				echo substr($directorsOut, 0, -2);
				
				echo '<br>Writer: ';
				
				$writers = explode(', ',$row->writer);
				$writersOut = '';
				foreach ($writers as $w) {
					$writersOut .= '<a href="index.php?c=writer&q='.$w.'">'.$w.'</a>, ';
				}
				echo substr($writersOut, 0, -2);
				
				echo '<br>Actors: ';
				
				$actors = explode(', ',$row->actors);
				$actorsOut = '';
				foreach ($actors as $a) {
					$actorsOut .= '<a href="index.php?c=actors&q='.$a.'">'.$a.'</a>, ';
				}
				echo substr($actorsOut, 0, -2);
							
				echo '</div>';
				
				echo '<div class="plotWrapper">';
				echo '<h3>Plot</h3>';
				echo '<p>'.$row->plot.'</p>';
				echo '</div>';
				
				echo '<div class="specWrapper">';
				echo '<p>' . $row->runtime . ', '.$row->votes . ' votes';
				
				$trailerArg = str_replace(' ', '%20', $row->title) . '('.$row->year.')';
				echo ', <a target="_blank" href="http://sharemovi.es/trailer.php?q='.$trailerArg.'">trailer</a>';
				echo ', <a target="_blank" href="http://www.imdb.com/title/'.$row->imdb.'">imdb</a></p>';
				echo '</div>';
								
				$counter++;
			}
		} else {
			echo "cannot retrieve movies";
		}
		?>
	</ul>
</body>
</html>
