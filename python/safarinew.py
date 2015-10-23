#!/usr/bin/python
import getopt
import os
import re
import sys
import smtplib
import urllib
from bs4 import BeautifulSoup as Soup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  

class SafariNew:

  def __init__(self, cache=False):
    self.cache = cache
    self.cacheFile = "safari_new.html"
    self.url = "https://www.safaribooksonline.com/explore/new/by-day/"
    self.soup = self._get_soup()
    self.items = self._parse_items()
    self.publisherQuery = "https://www.safaribooksonline.com/search/?query=SEARCH&field=publishers&sort=date_added&highlight=true"
    self.filters = { "title": None, "link": None, "author": None, "publisher": None, "added": 1, }

  def _get_soup(self):
    if self.cache: 
      if not os.path.isfile(self.cacheFile):
        try:
          urllib.urlretrieve(self.url, self.cacheFile) 
        except:
          sys.exit("cannot download html from %s" % self.url)
      f = open(self.cacheFile)
    else:
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
          if re.search(r'\b%s\b' % lf.lower(), item[lookIn].lower()):
            return True
    return False

  def generate_html(self, filters=None, printSource=True):
    out = ["<ul>"]
    for i in self.items:
      if self._title_new_enough(i["added"]) and self._pass_filters(i, filters):
        out.append("<li><a href='%s'>%s</a>&nbsp;&nbsp;[<a href='%s'>%s</a>]</li>\n" % \
          (i["link"], i["title"], self.publisherQuery.replace("SEARCH", urllib.quote(i["publisher"])), i["publisher"]))
    out.append("</ul>")
    if printSource:
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
    print "%s -c <cache file> -d <daily> -e <emails (comma separated)> -t <titles (comma separated)> -w <weekly>" % sys.argv[0]
    sys.exit()
  try:
    opts, args = getopt.getopt(sys.argv[1:],"hcdwe:t:")
  except getopt.GetoptError:
    usage()
  cache = daily = weekly = False
  emails = titles = []
  for opt, arg in opts:
    if opt == '-h':
      usage()
    elif opt == "-c":
      cache = True
    elif opt == "-d":
      daily = True
    elif opt == "-e":
      emails = arg.split(",") if "," in arg else [arg]
    elif opt == "-t":
      titles = arg.split(",") if "," in arg else [arg]
    elif opt == "-w":
      weekly = True

  if not daily and not weekly:
    usage()

  sn = SafariNew(cache=cache)
  if daily:
    sn.filters["added"] = 1
    content = sn.generate_html()
    print content
  elif weekly:
    sn.filters["added"] = 7
    if titles:
      content = "<h2>Filtering on title strings: %s</h2>\n" % " | ".join(titles)
      content += sn.generate_html(filters={"title": titles}, printSource=False) 
    else:
      content = sn.generate_html()
    print content
        
  if emails:
    dayStr = "day" if sn.filters["added"] == 1 else "%i days" % sn.filters["added"]
    subject = "New books added to Safari in the last %s" % dayStr 
    if titles:
      subject += " (filtered on %s)" % " | ".join(titles)
    sn.mail_html(emails, subject, content)
