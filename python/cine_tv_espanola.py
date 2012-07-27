#! /usr/bin/env python
# author: Bob Belderbos
# created: July 2012 
# purpose/exercise: generate a list of movies on tv in the next hours 
# Unix cron will pipe the output to my mail daily

import urllib2
from bs4 import BeautifulSoup as Soup

def getImdbApiLink(title):
	try:
		t = urllib2.quote(title)
	except: 
		t = title

	link = "http://www.imdbapi.com/?t="
	link += t 	
	return link


# http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
# or better replace this with re.sub
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

reps = {'images/logo_':'', '.jpg':''}



url = "http://parrilla-tv.lavanguardia.com/"
soup = Soup(urllib2.urlopen(url))
movies = soup.find_all("li", { "class" : "cine inactiu" })

for movie in movies: 
	try: 
		channel = replace_all(movie.parent.parent.parent.img.attrs['src'], reps)
		hour = movie.find_all("span", { "class" : "hora" })[0].get_text()
		title = movie.find_all("span", { "class" : "mes" })[0].get_text().split(': ')[1]

		# need to handle encoding better
		title = title.encode('ascii', 'ignore')

		print "%-12s / %-6s / %-50s" % (channel, hour, title )
		print getImdbApiLink(title) + "\n"
		
	except: 
		pass