#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Bob Belderbos / written: Dec 2012
# Purpose: get movies aired on Spanish tv to use in 24-hour cronjob
#
import pprint ;  pp = pprint.PrettyPrinter(indent=4)
import urllib, sys
from time import time
from bs4 import BeautifulSoup as Soup

class TvCine(object):

  def __init__(self):
    """ Setup """
    # show movies from 20-24 for now, todo: make these limits cli args
    self.START_TIME = 20
    self.END_TIME = 00
    self.moviePage = "http://www.sincroguia.tv/todas-las-peliculas.html" 
    self.movies = self.parse_movies()
    #pp.pprint(self.movies); sys.exit()


  def parse_movies(self):
    """ Import the movie URL """
    soup = Soup(urllib.urlopen(self.moviePage))
    movies = []
    for link in soup.find_all("a"):
      time = link.previous_sibling
      url = link.get('href')
      title = link.get('title')
      if not "/peliculas/" in url: continue
      if int(time[:2]) < self.START_TIME: continue
      if time[:2] == self.END_TIME: break
      (longTitle, verboseInfo) = self.get_movie_verbose_info(title, url)
      movies.append({ 'time': time[0:6], 
                      'title':longTitle.encode(encoding='UTF-8',errors='strict'), 
                      'url': url.encode(encoding='UTF-8',errors='strict'), 
                      'info': verboseInfo.encode(encoding='UTF-8',errors='strict'),  
                    })
    return movies

   
  def get_movie_verbose_info(self, title, url):
    html = self.read_url(url)
    soup = self.filter_relevant_bits(html)
    titleInfo = ficha = contentficha = ""; lineNum = 0
    for line in soup.li.stripped_strings: 
      ficha += line + "\n"
    for line in soup.find_all('li')[1].stripped_strings:
      lineNum += 1
      if lineNum<3: titleInfo += line
      contentficha += line + "\n"
    # somtimes there is not a translated title, in that case echo the original title
    titleInfo = titleInfo.replace("(", " (") if "(" in titleInfo else title
    return (titleInfo, ficha+"\n"+contentficha)


  def read_url(self, url):
    f = urllib.urlopen(url) 
    html = f.read()
    f.close
    return html

  
  def filter_relevant_bits(self, html):
    a = html.split('class="ficha">')
    movieInfo = a[1].split('<a href="javascript:;" onclick="remote')
    soup = Soup(movieInfo[0]) 
    return soup


  def print_movie_titles(self): 
    for m in self.movies:
      print m['time'], m['title']
      

  def print_movie_details(self):
    for m in self.movies:
      print "+" * 110
      print m['time'], m['title']
      print "+" * 110
      print "URL: \n" + m['url']
      print "\nDetails: \n" + m['info']
      print "\n\n"


### instant
t = TvCine()
t.print_movie_titles()
t.print_movie_details()
