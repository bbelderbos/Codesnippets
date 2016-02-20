CREATE TABLE IF NOT EXISTS `movie_collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) binary DEFAULT NULL,
  `year` varchar(128) binary DEFAULT NULL,
  `rated` varchar(128) binary DEFAULT NULL,
  `released` varchar(128) binary DEFAULT NULL,
  `genre` varchar(128) binary DEFAULT NULL,
  `director` varchar(128) binary DEFAULT NULL,
  `writer` varchar(128) binary DEFAULT NULL,
  `actors` varchar(128) binary DEFAULT NULL,
  `plot` varchar(500) binary DEFAULT NULL,
  `poster` varchar(500) binary DEFAULT NULL,
  `runtime` varchar(128) binary DEFAULT NULL,
  `rating` varchar(128) binary DEFAULT NULL,
  `votes` varchar(128) binary DEFAULT NULL,
  `imdb` varchar(128) binary DEFAULT NULL,
  `tstamp` varchar(128) binary DEFAULT NULL,
  PRIMARY KEY (`id`)
) TYPE=MyISAM AUTO_INCREMENT=1 ;
