#!/usr/bin/env python
# -*- coding: latin-1 -*-

import urllib, json
from pprint import pprint
from bs4 import BeautifulSoup as Soup

def getImdbInfo(title): 
	title = urllib.quote(title)
	imdbapiUrl = 'http://imdbapi.com/?t=%s' % title
	json_data=urllib.urlopen(imdbapiUrl)
	data = json.load(json_data)
	json_data.close()   
	return data



url = "http://www.laguiatv.com/programacion/la-sexta-3"
soup = Soup(urllib.urlopen(url))
movies = soup.find(id="emisiones").find_all("div")

for movie in movies: 
	movieName = movie.li.p.get_text().encode('latin-1')
	if "Teletienda" in movieName or "Todo cine" in movieName: 
		continue

	startTime = movie.li.time.get_text()
	print "Movie: " + movieName + "<br>"
	print "Starts: " + startTime + "<br>"

	try: 
		data = getImdbInfo(movieName)
		print "<br>==<br>"
		print "From IMDB API: <br>"
		print "Title: " + data['Title'].encode('latin-1') + "<br>"
		print "Year: " + data['Year']  + "<br>"
		print "Genre: " + data['Genre']  + "<br>"
		print "Director: " + data['Director']  + "<br>"
		print "Actors: " + data['Actors']  + "<br>"
		print "Plot: " + data['Plot']  + "<br>"
		if not "N/A" in data['Poster']:
			print "Poster: <a href='" + data['Poster']  + "' target='_blank'>here</a><br>"
		print data['imdbRating'] + " (" + data['imdbVotes'] + " votes)<br>"
		print "IMDB: <a href='http://imdb.com/title/" + data['imdbID'] + "' target='_blank'>http://imdb.com/title/" + data['imdbID'] + "</a><br>"

	except: 
		print "Cannot get IMDB API info<br>"

	print "==<br><br>"
