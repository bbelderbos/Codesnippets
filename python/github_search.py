#!/usr/bin/env python                                                                                                                                     
# -*- coding: utf-8 -*-
# Author: Bob Belderbos / written: Dec 2012
# Purpose: have an interactive github cli search app
#
import re, sys, urllib, pprint
# import html2text # -- to use local version

class GithubSearch:
  """ This is a command line wrapper around Github's Advanced Search
      https://github.com/search """

  def __init__(self):
    """ Setup variables """
    self.searchTerm = ""
    self.scripts = []
    self.show_menu()


  def show_menu(self):
    """ Show a menu to interactively use this program """
    prompt = """
      (N)ew search
      (S)how more context (github script)
      (Q)uit
      Enter choice: """
    while True:
      chosen = False 
      while not chosen:
        try:
          choice = raw_input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
          choice = 'q'
        except:
          sys.exit("Not a valid option")
        print '\nYou picked: [%s]' % choice 
        if choice not in 'nsq':
          print "This is an invalid option, try again"
        else:
          chosen = True
      if choice == 'q': sys.exit("Goodbye!")
      if choice == 'n': self.new_search() 
      if choice == 's': self.show_script_context()

  
  def new_search(self):
    """ Take the input field info for the advanced git search """
    # reset script url tracking list and counter
    self.scripts = [] 
    self.counter = 0
    # take user input to define the search
    try:
      self.searchTerm = raw_input("Enter search term: ").strip().lower().replace(" ", "+")
    except:
      sys.exit("Error handling this search term, exiting ...")
    lang = raw_input("Filter on programming language (press Enter to include all): ").strip().lower()
    try:
      prompt = "Number of search pages to process (default = 3): "
      numSearchPages = int(raw_input(prompt).strip()[0])
    except:
      numSearchPages = 3
    # get the search results
    for page in range(1,numSearchPages+1):
      results = self.get_search_results(page, lang)
      for result in results[1].split("##"): # each search result is divided by ##
        self.parse_search_result(result)


  def get_search_results(self, page, lang):
    """ Query github's advanced search and re.split for the relevant piece of info 
        RFE: have a branch to use html2text local copy if present, vs. remote if not """
    githubSearchUrl = "https://github.com/search?q="
    searchUrl = urllib.quote_plus("%s%s&p=%s&ref=searchbar&type=Code&l=%s" % \
      (githubSearchUrl, self.searchTerm, page, lang))
    html2textUrl = "http://html2text.theinfo.org/?url="
    queryUrl = html2textUrl+searchUrl
    html = urllib.urlopen(queryUrl).read()
    return re.split(r"seconds\)|## Breakdown", html)


  def parse_search_result(self, result):
    """ Process the search results, also store each script URL in a list for reference """
    lines = result.split("\n")
    source = "".join(lines[0:2])
    pattern = re.compile(r".*\((.*?)\)\s+\((.*?)\).*")
    m = pattern.match(source)
    if m != None:
      self.counter += 1 
      url = "https://raw.github.com%s" % m.group(1).replace("tree/", "")
      lang = m.group(2)
      self.print_banner(lang, url)
      self.scripts.append(url) # keep track of script links 
      for line in lines[2:]:
        # ignore pagination markup
        if "github.com" in line or "https://git" in line or "[Next" in line: continue 
        if line.strip() == "": continue
        print line


  def print_banner(self, lang, url):
    """ Print the script, lang, etc. in a clearly formatted way """
    print "\n" + "+" * 125
    print "(%i) %s / src: %s" % (self.counter, lang, url)


  def show_script_context(self, script_num=""):
    """ Another menu option to show more context from the github script 
        surrounding or leading up to the search term """
    if len(self.scripts) == 0:
      print "There are no search results yet, so cannot show any scripts yet."
      return False
    script_num = int(raw_input("Enter search result number: ").strip())
    script = self.scripts[script_num-1] # list starts with index 0 = 1 less than counter
    a = urllib.urlopen(script)
    if a.getcode() != 200:
      print "The requested script did not give a 200 return code"
      return False
    lines = a.readlines() 
    a.close()
    if len(lines) == 0:
      print "Did not get content back from script, maybe it is gone?"
      return False
    num_context_lines = 8
    print "\nExtracting more context for search term <%s> ..." % self.searchTerm
    print "Showing %i lines before and after the match in the original script hosted here:\n%s\n" % \
      (num_context_lines, script)
    for i, line in enumerate(lines):
      if self.searchTerm.lower() in line.lower():
        print "\n... %s found at line %i ..." % (self.searchTerm, i)
        j = i - num_context_lines
        for x in lines[i-num_context_lines : i+num_context_lines]:
          if self.searchTerm.lower() in x.lower():
            print "%i ---> %s" % (j, x), # makes the match stand out
          else:
            print "%i      %s" % (j, x),        
          j += 1


### instant
github = GithubSearch()
