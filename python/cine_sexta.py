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

	return (data['Title'], data['Year'], data['imdbID'])



url = "http://www.laguiatv.com/programacion/la-sexta-3"
soup = Soup(urllib.urlopen(url))
movies = soup.find(id="emisiones").find_all("div")

for movie in movies: 
	movieName = movie.li.p.get_text().encode('latin-1')
	startTime = movie.li.time.get_text()
	print startTime,
	print movieName

	try: 
		(orgTitle, year, imdb) = getImdbInfo(movieName)
	except: 
		(orgTitle, year, imdb) = ''

	print orgTitle.encode('latin-1')
	print year
	print "http://imdb.com/title/",
	print imdb 
	print "==\n"
