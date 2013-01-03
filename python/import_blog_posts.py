#!/usr/bin/env python                                                                                                                                     
# -*- coding: utf-8 -*-
# Author: Bob Belderbos / written: Dec 2012
# Purpose: import all blog posts to one file, converting them in (markdown) text
# Thanks to html2text for doing the actual conversion ( http://www.aaronsw.com/2002/html2text/ ) 
# 
import os, sys, pprint, xml.dom.minidom, urllib, html2text, subprocess

class ImportBlogPosts(object):
  """ Import all blog posts and create one big text file (pdf would increase size too much,
      and I like searching text files with Vim).  It uses the blog's sitemap to get all URLs. """

  def __init__(self, url, poststart, postend, sitemap="sitemap.xml"):
    """ Specify blog url, where post html starts/ stops, what urls in sitemap are valid, and sitemap """
    self.sitemap = sitemap
    self.sitemapUrl = "%s/%s" % (url, self.sitemap)
    self.postStartMark = poststart # where does post content html start?
    self.postEndMark = postend # where does post content html stop?
    if not os.path.isfile(self.sitemap):
      cmd = "wget -q %s" % self.sitemapUrl
      if subprocess.call(cmd.split()) != 0:
        sys.exit("No 0 returned from %s, exiting ..." % cmd)
    self.blogUrls = self.parse_sitemap(self.sitemap)

      
  def parse_sitemap(self, sitemap):
    """ Parse blog's specified xml sitemap """
    posts = {}
    dom = xml.dom.minidom.parse(sitemap)
    for element in dom.getElementsByTagName('url'):
      url = self.getText(element.getElementsByTagName("loc")[0].childNodes)
      mod = self.getText(element.getElementsByTagName("lastmod")[0].childNodes)
      posts[url] = mod # there can be identical mods, but urls are unique
    urls = []
    # return urls ordered desc on last mod. date
    for key, value in sorted(posts.iteritems(), reverse=True, key=lambda (k,v): (v,k)):
      urls.append(key)
    return urls


  def getText(self, nodelist):
    """ Helper method for parsing XML childnodes (see parse_sitemap) """
    rc = ""
    for node in nodelist:
      if node.nodeType == node.TEXT_NODE:
        rc = rc + node.data
    return rc

  
  def import_post_urls(self, urlCriteria="http"):
    """ Loop over blog URL getting each one's content, default 'http' practically results in importing all links """
    for i, url in enumerate(self.blogUrls):
      if urlCriteria in url: 
        html = self.get_url(url)
        if html != None:
          self.print_banner(i, url)
          self.print_content(url)
  

  def get_url(self, url):
    """ Import html from specified url """
    try:
      f = urllib.urlopen(url)
      html = f.read()
      f.close()
      return html
    except: 
      print "Problem getting url %s" % url
      return None


  def print_banner(self, i, url):
    """ print a banner for a specified URL (to seperate from content) """
    divider = "+"*120
    print "\n\n"
    print divider
    print "%i) %s" % (i, url)
    print divider
    print "\n"


  def print_content(self, url): 
    """ Get blog post's content, get relevant html, then convert to plain text """
    try:
      # I know, I probably should have used urllib.urlopen but somehow it 
      # it doesn't import the body html, so using good 'ol wget as workaround
      cmd = "wget -q -O - %s" % url
      html = subprocess.check_output(cmd.split())
    except subprocess.CalledProcessError as e:
      print "Something went wrong importing %s, error: %s" % (url, e)
      return False
    postContent = self.filter_post_content(html)
    if postContent == None:
      print "postContent == None, something went wrong in filter_post_content?"
    else:
      try:
        # to print in terminal decode to utf-8 needed, to print and redirect
        # script's output to file with >, that only works with ascii encode
        postContent = postContent.decode('utf-8')
        print html2text.html2text(postContent).encode('ascii', 'ignore') 
      except:
        print "Cannot convert this post's html to plain text"


  def filter_post_content(self, textdata):
    """ Takes the post page html and return the post html body """
    try:
      post = textdata.split(self.postStartMark)
      post = "".join(post[1:]).split(self.postEndMark)
      return post[0]
    except:
      print "Cannot split post content based on specified start- and endmarks"
      return None

# end class


### run this program from cli
import optparse
parser = optparse.OptionParser()
parser.add_option('-u', '--url', help='specify a blog url', dest='url')
parser.add_option('-b', '--beginhtml', help='first html (div) tag of a blog post', dest='beginhtml')
parser.add_option('-e', '--endhtml', help='first html after the post content', dest='endhtml')
parser.add_option('-s', '--sitemap', help='sitemap name, default = sitemap.xml', dest='sitemap', default="sitemap.xml")
parser.add_option('-p', '--posts', help='url string to filter on, e.g. "/2012" for all 2012 posts', dest='posts', default="http")
(opts, args) = parser.parse_args()

# Making sure all mandatory options appeared.
mandatories = ['url', 'beginhtml', 'endhtml']
for m in mandatories:
  if not opts.__dict__[m]:
    print "Mandatory option is missing\n"
    parser.print_help()
    exit(-1)

# Execute program with given cli options: 
blog = ImportBlogPosts(opts.url, opts.beginhtml, opts.endhtml, opts.sitemap)
blog.import_post_urls(opts.posts)



### example class instant. syntax, and using it for other blogs
# + instant class
# blog = ImportBlogPosts("http://bobbelderbos.com", '<div class="entry-content">', '<div><br /><h4><strong>You might also like:')
# + all posts my blog:
# blog.import_post_urls("/20")
# + only one post my blog:
# blog.import_post_urls('http://bobbelderbos.com/2012/09/how-to-grow-craft-programming/')
# + another single post on my blog:
# blog.import_post_urls('http://bobbelderbos.com/2012/10/php-mysql-novice-to-ninja/')
# 
# + other blogs:
# blog = ImportBlogPosts("http://zenhabits.net", '<div class="entry">', '<div class="home_bottom">', "zenhabits.xml") 
# blog = ImportBlogPosts("http://blog.extracheese.org/", '<div class="post content">', '<div class="clearfix"></div>', "/Users/bbelderbos/Downloads/gary.xml") 
# + import all urls
# blog.import_post_urls()
# blog = ImportBlogPosts("http://programmingzen.com", '<div class="post-wrapper">', 'related posts', "/Users/bbelderbos/Downloads/programmingzen.xml") 
# + supposedly all posts
# blog.import_post_urls("/20")
