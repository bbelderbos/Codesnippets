#!/usr/bin/python
import getopt
import os
import re
import sys
import smtplib
import time
import urllib
from bs4 import BeautifulSoup as Soup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  

class SafariNew:

  def __init__(self, cache, refreshCache):
    self.cache = cache
    self.refreshCache = refreshCache
    self.cacheFile = "safari_new.html"
    self.secInDay = 24*60*60
    self.now = int(time.time())
    self.url = "https://www.safaribooksonline.com/explore/new/by-day/"
    self.soup = self._get_soup()
    self.items = self._parse_items()
    self.publisherQuery = "https://www.safaribooksonline.com/search/?query=SEARCH&field=publishers&sort=date_added&highlight=true"
    self.filters = { "title": None, "link": None, "author": None, "publisher": None, "added": 1, } # TODO make lookback a cli arg too

  def _cache_outdated(self):
    st=os.stat(self.cacheFile)
    cacheCreated = int(st.st_mtime)
    renew = (self.now - cacheCreated) > self.secInDay
    if renew: 
      print "Cache file expired, downloading a new copy ..."
    return renew

  def _download_new_cache_file(self):
    try:
      urllib.urlretrieve(self.url, self.cacheFile) 
    except:
      sys.exit("cannot download html from %s" % self.url)

  def _refresh_cache_file(self):
    if self.refreshCache: 
      print "Refresh cache option choosen, downloading new cache file"
      self._download_new_cache_file()
    elif self.cache and not os.path.isfile(self.cacheFile): 
      print "Cache option choosen, but no cache file, downloading new cache file"
      self._download_new_cache_file()
    elif self.cache and self._cache_outdated():
      print "Cache option choosen, but cache file is outdated, downloading new cache file"
      self._download_new_cache_file()

  def _get_soup(self):
    if self.refreshCache or self.cache: 
      print "Using cached option"
      self._refresh_cache_file()
      f = open(self.cacheFile)
    else:
      print "Using live URL (no cache)"
      f = urllib.urlopen(self.url)
    try:
      soup = Soup(f, 'html5lib') # needed otherwise incomplete html parsing (div class 'list-item')
    except IOError:
      sys.exit("Cannot retrieve %s" % self.url) 
    f.close()
    return soup

  def _parse_items(self):
    items = []
    for div in self.soup.find_all("li", {"class": "list-item"}):
      title = div.find("div", {"class" : "title"}).get_text(strip=True)
      link = div.find("div", {"class" : "title"}).find("a", href=True)["href"] 
      author = div.find("div", {"class" : "byline"}).get_text(strip=True)
      publisher = div.find("div", {"class" : "metadata"}).get_text(strip=True)
      added = div.find("div", {"class" : "status"}).get_text(strip=True)
      items.append({
        "title" : title,
        "link" : link,
        "author" : author,
        "publisher" : publisher,
        "added" : added,
      })
    return items

  def _title_new_enough(self, titleAdded):
    m = re.search(r'.*(\d+).*', titleAdded)
    if not m:
      return False
    timeAgo = int(m.groups()[0])
    lookBackDays = self.filters["added"]
    if "hour" in titleAdded: # hours is always fresh enough
      return True
    if "day" in titleAdded and timeAgo < lookBackDays:
      return True
    if "week" in titleAdded and lookBackDays > 6: # only 1 week on page so then return all
      return True 
    return False

  def _pass_filters(self, item, filters):
    if not filters:
      return True
    for lookIn,lookFor in filters.items():
      if lookIn in item: 
        for lf in lookFor: 
          if " " in lf: # e.g. "big data"
            if re.search(r'%s' % lf.lower(), item[lookIn].lower()): 
              return True
          else:
            if re.search(r'\b%s\b' % lf.lower(), item[lookIn].lower()): # java (need word boundary to not hit javascipt)
              return True
    return False

  def generate_html(self, filters=None):
    out = ["<ul>"]
    for i in self.items:
      if self._title_new_enough(i["added"]) and self._pass_filters(i, filters):
        out.append("<li><a href='%s'>%s</a>&nbsp;&nbsp;[<a href='%s'>%s</a>]</li>\n" % \
          (i["link"], i["title"], self.publisherQuery.replace("SEARCH", urllib.quote(i["publisher"])), i["publisher"]))
    out.append("</ul>")
    out.append("<p>Source: <a href='https://www.safaribooksonline.com/explore/new/by-day/'>Safari new by day</a></p>")
    return "\n".join(out).encode('ascii', 'ignore')

  def mail_html(self, recipients, subject, content):
    sender = "info@bobbelderbos.com"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    part = MIMEText(content, 'html')
    msg.attach(part)
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()


if __name__ == "__main__":
  def usage():
    print "\nUsage: %s" % sys.argv[0]
    print "-c : use cached html (for testing)"
    print "-d : see what was added in the last day"
    print "-e : send parsed HTML output to comma separated list of emails"
    print "-h : print this help"
    print "-p : filter on a comma separated list of publishers"
    print "-r : refresh the cached html file"
    print "-t : filter on a comma separated list of titles"
    print "-w : see what was added the last week"
    print "\nNote: "
    print "* -d and -w are mutually exclusive"
    print "* -t only works with -w (weekly report)"
    print "* -c refreshes the cache file if older than 24 hours, use -r to forcefully refresh it"
    sys.exit()
  try:
    opts, args = getopt.getopt(sys.argv[1:],"cde:hp:rt:w")
  except getopt.GetoptError:
    usage()
  (cache, daily, emails, publisherFilters, refreshCache, titleFilters, weekly) = \
    (False, False, [], [], False, [], False)
  for opt, arg in opts:
    if opt == '-h':
      usage()
    elif opt == "-c":
      cache = True
    elif opt == "-d":
      daily = True
    elif opt == "-e":
      emails = arg.split(",") if "," in arg else [arg]
    elif opt == "-p":
      publisherFilters = arg.split(",") if "," in arg else [arg]
    elif opt == "-r":
      refreshCache = True
    elif opt == "-t":
      titleFilters = arg.split(",") if "," in arg else [arg]
    elif opt == "-w":
      weekly = True

  if not daily and not weekly: 
    print "WARNING: need at least -d or -w"
    usage()
  elif daily and weekly:
    print "WARNING: -d and -w are mutually exclusive"
    usage()

  sn = SafariNew(cache=cache, refreshCache=refreshCache)
  content = ""

  if daily:
    print "Daily option choosen, looking 1 day back"
    sn.filters["added"] = 1
    content = sn.generate_html()
  elif weekly:
    print "Weekly option choosen, looking 7 days back"
    sn.filters["added"] = 7

  if titleFilters:
    print "Title filter(s) specified, using filters"
    content = sn.generate_html(filters={"title": titleFilters})
  elif publisherFilters:
    print "Publisher filter(s) specified, using filters"
    content = sn.generate_html(filters={"publisher": publisherFilters})
  else:
    print "No filter(s) specified, printing all"
    content = sn.generate_html()

  if emails:  
    dayStr = "day" if sn.filters["added"] == 1 else "%i days" % sn.filters["added"]
    subject = "New books added to Safari in the last %s" % dayStr 
    if titleFilters:
      subject += " (filtering titles on %s)" % " | ".join(titleFilters).lower()
    elif publisherFilters:
      subject += " (filtering publishers on %s)" % " | ".join(publisherFilters).lower()
    print "Email(s) specified, sending email to: %s with subject '%s'" % (", ".join(emails), subject)
    sn.mail_html(emails, subject, content)

  print "\n\n == Parsed content ==\n" + content
  print "\n== end ==\n"
