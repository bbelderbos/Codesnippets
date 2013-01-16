#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Bob Belderbos 
# V1: Mar 2012 / V2: Jan 2013
# Purpose: script to import tweet history via twitter's timeline pagination
# Blog post: http://bobbelderbos.com/2012/03/a-simple-script-to-archive-your-tweets/
#
import re, sys, urllib, simplejson, time, datetime, calendar, pprint

if(len(sys.argv) < 3):
  sys.exit("Usage: %s <twitter handle> <max tweets>" % sys.argv[0])

user = sys.argv[1]
maxTweets = sys.argv[2]
verbose = True # turn off to not get the _err log
resultsPerPage = 100 # user_timeline shows 200 results as max, but you often get less
numQueries = int(maxTweets) / resultsPerPage
baseUrl = "https://api.twitter.com/1/statuses/user_timeline/";
queryString = "%s.json?count=%s&page=" % (str(user), str(resultsPerPage)) 
statusUrl = "https://twitter.com/bbelderbos/status/"
tstampPattern = re.compile(r"\w+?\s(\w+?)\s+(\d+?)\s+(\d+?):(\d+?):(\d+?)\s+\S+?\s+(20\d+)")
monthNames = dict((v,k) for k,v in enumerate(calendar.month_abbr))
tweets = {}
debugOut = ""
filename = "tweet_archive_%s_%s.txt" % (user, str(int(time.time()))) # err out depends on this filename

for pageNum in range(numQueries):
  queryUrl = baseUrl + queryString + str(pageNum)
  debugOut += "MSG: getting results from %s\n" % queryUrl
  result = simplejson.load(urllib.urlopen(queryUrl))
  if not result:
    debugOut += "ERROR: no result for %s\n" % queryUrl
  for tweet in result:
    # todo why dont I get result??
    #print tweet['created_at']; continue
    # end todo
    m = tstampPattern.match(tweet['created_at'])
    if m.groups() != None:
      d = datetime.datetime(
        int(m.group(6)), 
        int(monthNames[m.group(1)]), 
        int(m.group(2)), 
        int(m.group(3)), 
        int(m.group(4)), 
        int(m.group(5)), 
        0)
      tweetId = str(int(time.mktime(d.timetuple())))
    else: 
      print "MSG cannot convert time %s\n" % tweet['created_at']
      
    if tweetId in tweets: 
      debugOut += "WARNING: TweetId %s already appeared in tweets dict\n" % tweetId
      continue
    output = "="*110 + "\n"
    output += "* Tweet: %s\n" % tweet['text'].encode("utf-8")
    output += "* When: %s / Tweet URL: %s%s\n" % (tweet['created_at'], statusUrl, str(tweet['id_str']) )
    output += "* Stats: # Fav: %s / # RT: %s\n" % (tweet['favorited'], tweet['retweet_count'])
    output += "\n"
    tweets[tweetId] = output
  # if pageNum == 30: break # todo: need to check, last time it was max. 3200 tweets

try:
  f = open(filename, 'w')
  for key in reversed(sorted(tweets.iterkeys())):
    f.write(tweets[key])
  f.close()
except IOError as e:
  sys.exit("Cannot write output to %s: %s" % (filename, e))


print "Done!"
print "Output written to %s\n" % filename

if verbose:
  try:
    f = open(filename.replace('.txt', '_err.txt'), 'w')
    f.write(debugOut)
    f.close()
  except IOError as e:
    sys.exit("Cannot write output to %s: %s" % (filename, e))
