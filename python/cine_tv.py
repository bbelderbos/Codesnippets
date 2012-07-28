#!/usr/bin/env python
# -*- coding: latin-1 -*-

import urllib
from bs4 import BeautifulSoup as Soup

# http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

reps = {'images/logo_':'', '.jpg':''}

url = "http://parrilla-tv.lavanguardia.com/"
soup = Soup(urllib.urlopen(url))
movies = soup.find_all("li", { "class" : "cine inactiu" })

for movie in movies:  
	try:
		channel = replace_all(movie.parent.parent.parent.img.attrs['src'], reps)
		hour = movie.find_all("span", { "class" : "hora" })[0].get_text()
		title = " ".join(movie.find_all("span", { "class" : "mes" })[0].get_text().split(': ')[1:]).encode('latin-1')
		
		print channel + "<br>"
		print hour + "<br>" 
		print title + "<br>"
		print "<a href='http://imdbapi.com/?t=" + urllib.quote(title) +"' target='_blank'>http://imdbapi.com/?t=" + urllib.quote(title) + "</a><br>"
		print "==<br><br>"

	except: 
		pass