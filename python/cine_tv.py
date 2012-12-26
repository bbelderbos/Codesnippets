#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Bob Belderbos / written: Dec 2012
# Purpose: get movies aired on Spanish tv to use in 24-hour cronjob
#
import pprint, urllib, re, sys, datetime
from bs4 import BeautifulSoup as Soup

class TvCine(object):

  def __init__(self):
    """ Setup variables, define hour range of which I want to know the movie airing of """
    # if weekday (0-4 - 0 being Monday) show movies from 20-24h, weekend I want to see all movies aired: 
    self.weekday = datetime.datetime.today().weekday() 
    if self.weekday in [5,6]: # 5 = Sat, 6 = Sun
      self.START_TIME = 9
    else: 
      self.START_TIME = 20
    # always end at midnight (tomorrow a new day, so a new output from cron)
    self.END_TIME = 00
    self.moviePage = "http://www.sincroguia.tv/todas-las-peliculas.html" 
    self.movies = self.parse_movies()
    # pprint.pprint(self.movies); sys.exit()


  def parse_movies(self):
    """ Import the movie URL """
    soup = Soup(self.read_url(self.moviePage))
    movies = []
    for link in soup.find_all("a"):
      time = link.previous_sibling
      try:
        channel = re.sub(r".* - ", "", str(link.contents[0].encode(encoding='UTF-8',errors='strict')))
      except:
        channel = "not_found" 
      url = link.get('href')
      title = link.get('title')
      if not "/peliculas/" in url: continue
      if int(time[:2]) < self.START_TIME: continue
      if time[:2] == self.END_TIME: break
      (longTitle, verboseInfo) = self.get_movie_verbose_info(title, url)
      movies.append({ 'time': time[0:6], 
                      'channel': channel,
                      'title':longTitle.encode(encoding='UTF-8',errors='strict'), 
                      'url': url.encode(encoding='UTF-8',errors='strict'), 
                      'info': verboseInfo.encode(encoding='UTF-8',errors='strict'),  
                    })
    return movies

   
  def get_movie_verbose_info(self, title, url):
    """ Read the movie page in and return the translated title if available and all movie info """
    html = self.read_url(url)
    # try to get the relevant html section of the movie page, if nothing found too bad, move on
    soup = self.filter_relevant_bits(html)
    titleInfo = ficha = contentficha = ""; lineNum = 0
    if soup: 
      for line in soup.li.stripped_strings: 
        ficha += line + "\n"
      for line in soup.find_all('li')[1].stripped_strings:
        lineNum += 1
        if lineNum<3: titleInfo += line
        contentficha += line + "\n"
      # somtimes there is not a translated title, in that case echo the original title
      titleInfo = titleInfo.replace("(", " (") if "(" in titleInfo else title
    else:
      ficha = "Not able to obtain movie info for %s" % title
    return (titleInfo, ficha+"\n"+contentficha)


  def read_url(self, url):
    """ Read and return the content of a url """
    f = urllib.urlopen(url) 
    html = f.read()
    f.close
    return html

  
  def filter_relevant_bits(self, html):
    """ Get the html part that matters from the movie page """
    a = html.split('class="ficha">')
    try:
      movieInfo = a[1].split('<a href="javascript:;" onclick="remote')
    except IndexError:
      return False 
    soup = Soup(movieInfo[0]) 
    return soup


  def print_movie_titles(self): 
    """ Print all the movie titles to be aired on Spanish TV today """
    print "I. Movies Spanish TV Today %s:00-%s:00\n" % (self.START_TIME, self.END_TIME)
    for m in self.movies:
      print m['time'], " | ", "%-8s" % m['channel'], " | ", m['title']
    print "\n\n"
      

  def print_movie_details(self):
    """ Print verbose details for each movie """
    print "II. Details for each movie ... \n" 
    for m in self.movies:
      print "+" * 80
      print m['time'], " | ", "%-8s" % m['channel'], " | ", m['title']
      print "+" * 80
      print "URL: \n" + m['url']
      print "\nDetails: \n" + m['info']
      print "\n\n"


### instant
t = TvCine()
t.print_movie_titles()
t.print_movie_details()
