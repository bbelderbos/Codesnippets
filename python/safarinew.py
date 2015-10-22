#!/usr/bin/python
import os
import re
import sys
import smtplib
import urllib
from bs4 import BeautifulSoup as Soup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  

class SafariNew:

  def __init__(self):
    self.page = "https://www.safaribooksonline.com/explore/new/by-day/"
    try:
      self.soup = Soup(urllib.urlopen(self.page), 'html5lib') # needed otherwise incomplete html parsing (div class 'list-item')
    except IOError:
      sys.exit("Cannot retrieve %s" % self.page) 
    self.items = self._parse_items()
    self.publisherQuery = "https://www.safaribooksonline.com/search/?query=SEARCH&field=publishers&highlight=true"
    self.filters = { "title": None, "link": None, "author": None, "publisher": None, "added": 1, }

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

  def show_items(self, filters=None):
    out = ["<ul>"]
    for i in self.items:
      if self._title_new_enough(i["added"]):
        out.append("<li><a href='%s'>%s</a>&nbsp;&nbsp;[<a href='%s'>%s</a>]</li>\n" % \
          (i["link"], i["title"], self.publisherQuery.replace("SEARCH", urllib.quote(i["publisher"])), i["publisher"]))
    out.append("</ul>")
    return "\n".join(out).encode('ascii', 'ignore')

  def mail_html(self, recipients, content):
    sender = "info@bobbelderbos.com"
    msg = MIMEMultipart('alternative')
    dayStr = "day" if self.filters["added"] == 1 else "%i days" % self.filters["added"]
    msg['Subject'] = "New books added to Safari in the last %s" % dayStr 
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    part = MIMEText(content, 'html')
    msg.attach(part)
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()


if __name__ == "__main__":
  sn = SafariNew()
  content = sn.show_items()
  recipients = ["bobbelderbos@gmail.com", "sequeira.julian@gmail.com", ]
  sn.mail_html(recipients, content)
