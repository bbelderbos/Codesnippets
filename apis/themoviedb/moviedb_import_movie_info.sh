#!/bin/bash
# author: bob belderbos
# purpose: 
# this script takes all valid themoviedb.org URLs (moviedb_get_valid_urls.sh)
# and gets movie info, cast and keywords. 
# api limits: http://help.themoviedb.org/kb/general/api-request-limits
# when testing this script did < 3 seconds per second so I didn't put code in
# for now to check this and sleep the necessary time between requests. 
# I also write the raw json output to a file, to convert it into sql import
# statements with a new script


# I want to measure the time this takes
# see http://stackoverflow.com/questions/5939646/elapsed-time-for-each-rule
function timer()
{
	if [[ $# -eq 0 ]]; then
	  echo $(date '+%s')
	else
	  local  stime=$1
	  etime=$(date '+%s')

	  if [[ -z "$stime" ]]; then stime=$etime; fi

	  dt=$((etime - stime))
	  ds=$((dt % 60))
	  dm=$(((dt / 60) % 60))
	  dh=$((dt / 3600))
	  printf '%d:%02d:%02d' $dh $dm $ds
	fi
}
t=$(timer)



# need file with valid IDs, point is this saves requests
# this is the output file defined in moviedb_get_valid_urls.sh
#
# I did a test on almost 120.000 movies to find out that 31710 ids gave 404
# and 88128 were valid, so yes not making one third of the requests saves time 

if [ $# -lt 1 ]; then
	echo "Input file with valid movie IDs"
	exit
fi

valid_movies_input_file=$1

# does the file exists here?
if [ ! -f $valid_movies_input_file ]; then
	echo "File $valid_movies_input_file not found, exiting ..."
	exit
fi



# need api key to query themoviedb
moviedb_key="YOUR KEY"

# this gets the valid movie Ids ("= 0") that returned moviedb_get_valid_urls.sh
valid_movie_ids=`awk -F= '/ = 0/ {print $1}' $valid_movies_input_file`



# loop over them and get me 1. movie info, 2. cast, 3. keywords
# saving this to 3 files
for i in $valid_movie_ids; 
	do
		cmd="curl -s http://api.themoviedb.org/3/"
		${cmd}movie/$i?api_key=$moviedb_key >> get_movie_info
		${cmd}movie/$i/casts?api_key=$moviedb_key >> get_movie_cast
		${cmd}movie/$i/keywords?api_key=$moviedb_key >> get_movie_keywords
	done



# how long did it take? 
printf 'Elapsed time: %s\n' $(timer $t)
