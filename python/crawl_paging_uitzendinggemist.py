#! /usr/bin/env python
# author: Bob Belderbos
# created: April 2012 
# purpose/exercise: crawl paging of uitzendinggemist.nl to get all RSS feeds of programs
# target url: http://www.uitzendinggemist.nl/programmas/

import urllib
from bs4 import BeautifulSoup as Soup

for page in range(1, 93):
  soup = Soup(urllib.urlopen("http://www.uitzendinggemist.nl/programmas/?page=" + str(page)))

  for link in soup.find_all(attrs={'class': 'knav_link'}):
    print link.get('title').encode("utf-8")," :: ",
    print "http://www.uitzendinggemist.nl" + link.get('href') + ".rss"