#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import re

filename = "index.html"
podcast_url = "http://fourhourworkweek.com/podcast/"

# http://stackoverflow.com/questions/24346872/python-equivalent-of-a-given-wget-command
def get_index():
  attempts = 0
  while attempts < 3:
    try:
      response = urllib2.urlopen(podcast_url, timeout = 5)
      content = response.read()
      f = open( filename, 'w' )
      f.write( content )
      f.close()
      break
    except urllib2.URLError as e:
      attempts += 1
      print type(e)

def parse_feed():
  res = {}
  # http://stackoverflow.com/questions/6213063/python-read-next
  with open(filename, 'r+') as f:
    for line in f:
      if not line.strip():
        continue
      if 'id="post-' in line: 
        mtags = tag.findall(line)
        tags = [t.lstrip("tag").replace("-", " ") for t in mtags]
        for t in tags:
          if "ferris" in t or "podcast" in t or "show" in t:
            continue
          if t not in res:
            res[t] = 0
          res[t] += 1
  return res

if __name__ == "__main__":
  get_index()
  tag = re.compile(r'tag-[^" ]+')
  date = re.compile(r'201\d/\d{2}/\d{2}')
  res = parse_feed()

  order = []
  for t, tot in res.items():
    order.append( (tot, "%-50s | %s" % (t, "+"*tot) ) )

  for (tot, line) in reversed(sorted(order)):
    if tot > 2:
      print line
