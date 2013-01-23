#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, socket, sys, urllib2, re, datetime, pprint, smtplib
from bs4 import BeautifulSoup as Soup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MovieDigest(object):

  def __init__(self):
    self.numPages = {"now-playing" : 2, "upcoming" : 4, }
    self.urls = {"now-playing" : [], "upcoming" : [], }
    [self.urls["now-playing"].append("http://www.themoviedb.org/movie/now-playing?page=%i"%i) for i in range(1,self.numPages['now-playing']+1)]
    [self.urls["upcoming"].append("http://www.themoviedb.org/movie/upcoming?page=%i"%i) for i in range(1,self.numPages['upcoming']+1)]
    self.baseurl = "http://sharemovi.es"
    self.moviedb = "http://themoviedb.org"
    self.year = datetime.date.today().year
    self.weekNum = str(datetime.date.today().isocalendar()[1])
    self.fname = "sharemovi.es_digest_%s_w%s.html" % (self.year, self.weekNum)
    self.digestTitle = "Sharemovi.es Digest - %s / Week %s" % (self.year, self.weekNum)
    self.digestLocation = "/Users/bbelderbos/CODE/sharemovies/moviedigest" 
    self.floc = "%s/%s" % (self.digestLocation, self.fname) 
    self.pattern = re.compile(r'.*?<a href="([^"]+)".*?<img.*?src="([^"]+)".*?<a.*?>([^<]+)</a>.*?rating".*?>([^<]+)<.*?genres">([^<]+)</p><p.*?cast">(.*?)</p>.*')
    if os.path.isfile(self.floc):
      f = open(self.floc, "r")
      self.html = f.read()
      f.close()
    else:
      if len(sys.argv) > 1: # if arg = genre given, filter on this genre
        self.genreFilter = sys.argv[1].lower().split()
      else:
        self.genreFilter = False
      self.get_digest()


  def get_url(self, url):
    data = None
    headers = {   'Accept-Language': 'en-us', } # otherwise I get results in Spanish
    req = urllib2.Request(url, data, headers)
    u = urllib2.urlopen(req)
    soup = Soup(u) # ; print soup.prettify()
    return soup


  def print_html(self):
    print self.html.encode('utf-8', 'ignore')


  def write_html(self):
    if not os.path.isfile(self.floc):
      f = open(self.floc, "w")
      f.write(self.html.encode('utf-8', 'ignore'))
      f.close()


  def get_digest(self):
    self.html = "<div id='content' style='font: 85%/1.6 Verdana, sans-serif;'>"
    self.html += "<h1 style='background-color: #840015;color: #fff;'><a href='%s'><img src='%s/i/banner.jpg'></a></h1>" % (self.baseurl, self.baseurl)
    self.html += "<h4>%s</h4>" % self.digestTitle
    for category in sorted(self.urls.keys()):
      self.html += "<h2 style='color: #900; padding: 5px; border-bottom: 1px solid #ddd;'>%s</h2>" % \
        category.replace("-", " ").upper()
      if self.genreFilter:
        self.html += "<h3>Filtering on %s</h3>" % self.genreFilter
      self.html += "<table>"
      for url in self.urls[category]:
        soup = self.get_url(url)
        first = soup.find_all(attrs={'class': 'first'}) # exception, only 1
        rest = soup.find_all(attrs={'class': 'w480'}) # 24 movies more
        links = first + rest
        for i, link in enumerate(links):
          link = "".join(str(link).split("\n"))
          m = self.pattern.match(link)
          if m == None: 
            continue
          [urlstr, poster, title, score, genres, cast] = [var.decode('utf-8') for var in m.groups()]
          themoviedbUrl  = "%s%s" % (self.moviedb, urlstr)
          sharemoviesUrl = "%s%s" % (self.baseurl, urlstr)
          if self.genreFilter and not list(set(self.genreFilter).intersection(set(genres.lower().split(", ")))):
            continue
          soupMovie = self.get_url(themoviedbUrl)
          overview = soupMovie.find_all(attrs={'id': 'overview'}) 
          self.html += "<tr style='border-bottom: 1px solid #ccc; margin: 10px; padding: 10px; font-size: 90%;'>" 
          self.html += "<td style='margin: 5px; vertical-align:top;'>"
          self.html += "<img style='width: 185px; border: 1px solid #ddd; padding: 5px;' src='%s'></td>" % \
            poster.replace("w92", "w185") # bigger size poster 
          self.html += "<td style='margin: 5px; vertical-align:top;'>"
          self.html += "<h4><a style='text-decoration: none; color: #900; padding: 10px 2px 5px 2px; font-size: 120%%;' href='%s'>%s</a></h4>" % \
            (sharemoviesUrl, title) 
          self.html += "<div style='padding: 4px;'>Genre: <b>%s</b><br>" % genres
          self.html += "Overview: %s<br>" % overview[0].string if overview else ""
          self.html += "Cast: %s<br>" % cast.replace("/person", "%s/person" % self.baseurl)
          self.html += "Score: <b>%s</b><br><br><br></div></td>" % score
          self.html += "</tr>" 
      self.html += "</table>"
    self.html += "</div>"


  def mail_html(self, toEmail):
    # from http://stackoverflow.com/questions/882712/sending-html-email-in-python
    me = "info@sharemovi.es"
    you = toEmail
    msg = MIMEMultipart('alternative')
    msg['Subject'] = self.digestTitle
    msg['From'] = me
    msg['To'] = you
    text = "Hi movie fan!\nThis is the plain-text version, you can see the html version here:\n"
    text += "http://sharemovi.es/moviedigest/%s" % self.fname
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(self.html, 'html')
    # According to RFC 2046, the last part of a multipart message, in this case the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()



### instant 
m = MovieDigest()
# m.print_html()
m.write_html()
m.mail_html("myname@mail.com")
