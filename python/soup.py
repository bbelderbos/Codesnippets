import sys, urllib2
from bs4 import BeautifulSoup as Soup

if len(sys.argv) < 2:
  sys.exit("Provide url")

url = sys.argv[1]

def get_url(url):
  data = None
  headers = {   'Accept-Language': 'en-us', }
  req = urllib2.Request(url, data, headers)
  u = urllib2.urlopen(req)
  soup = Soup(u)
  print soup.prettify()
  return soup

soup = get_url(url)
