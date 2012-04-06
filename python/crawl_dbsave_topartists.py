#! /usr/bin/env python
# author: Bob Belderbos
# created: April 2012 
# purpose/exercise: crawl top ranked artists data and insert results in a database table
# target url: http://www.musicrow.com/charts/top-ranking-country-artists/

import urllib
from bs4 import BeautifulSoup as Soup
from time import time
import MySQLdb

db = MySQLdb.connect("localhost","bob","cangetin","bobbelde_models" )
cursor = db.cursor()

url = "http://www.musicrow.com/charts/top-ranking-country-artists/"
soup = Soup(urllib.urlopen(url))

for row in soup.find_all(attrs={'class': 'row'}):
  artist = [text for text in row.stripped_strings]
  
  name = artist[1]
  followers = artist[5]
  likes = artist[7]
  
  thumb = row.select("img")[0]['src']
  twitter = row.select("a")[0]['href']
  facebook = row.select("a")[1]['href']
  tstamp = int(time())
  
  sql = """INSERT INTO top_ranking (id, name, followers, likes, thumb, 
          twitter, facebook, audit_who, audit_ins, audit_upd) VALUES
          (NULL, '%s', '%s', '%s', '%s', '%s', '%s', 'admin', '%d', NULL);
          """ % (name, followers, likes, thumb, twitter, facebook, tstamp )
  
  try:
    cursor.execute(sql)
    db.commit()
  except:
    db.rollback()
    db.close()
  

db.close()