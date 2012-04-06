#! /usr/bin/env python
# author: Bob Belderbos
# created: April 2012 
# purpose/exercise: crawl paging of uitzendinggemist.nl to get all RSS feeds of programs
# target url: http://www.uitzendinggemist.nl/programmas/

import urllib
from bs4 import BeautifulSoup as Soup
base_url = "http://www.uitzendinggemist.nl"
program_url = base_url + "/programmas/?page="

for page in range(1, 93):
  url =  "%s%d" % (program_url, page)
  soup = Soup(urllib.urlopen(url))

  for link in soup.find_all(attrs={'class': 'knav_link'}):
    print link.get('title').encode("utf-8")," :: ",
    print "%s%s.rss" % (base_url, link.get('href') )