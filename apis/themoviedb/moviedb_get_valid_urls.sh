#!/bin/bash
# author: bob belderbos
# purpose: 
# as preperation of importing all moviedb.org movie data, this scripts
# checks all movie IDs if they still have data. this saves the number
# of requests to the API and thus makes the whole import exercise faster

output_file="themoviedb_valid_ids.out"
moviedb_key="YOUR KEY"

if [ -f $output_file ]; then
	echo "$output_file already exist, move or delete it first."
	exit
fi

# to define the range of movieIds to check, themoviedb has 
# a method to get the latest movie added, see 
# http://help.themoviedb.org/kb/api/latest-movie

last_movie=`curl -s http://api.themoviedb.org/3/movie/latest?api_key=$moviedb_key|sed 's/.*id":\([0-9]*\),"imdb_id.*/\1/g' 2>/dev/null`


# loop over each movie ID and check for http return status, 0 = success
# and 1 is not found, append movie id and return status to the output file
# thanks zneak / http://stackoverflow.com/questions/2924422/how-do-i-determine-if-a-web-page-exists-with-shell-scripting#_=_

for ((i=1;i<=$last_movie;i++)); 
	do 
		curl -s --head http://www.themoviedb.org/movie/$i | head -n 1 | grep "HTTP/1.[01] [23].." > /dev/null
		echo "$i = $?" >> $output_file
	done