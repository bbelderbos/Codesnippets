#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, urllib, urllib2, pprint
from bs4 import BeautifulSoup as Soup

class StackoverflowCliSearch(object):
  """ Query stackoverflow from cli 
      I think this could be handy in Vim's spit view (with ConqueTerm) """

  def __init__(self):
    """ Definition class variables, initialize menu """
    self.searchTerm = ""
    self.questions = {}
    self.showNumAnswers = 1 # show 1 answer first, then 1 by 1 pressing N
    self.show_menu() # start user interaction


  def show_menu(self):
    """ Menu that allows user to to search, query question's answers, etc. """
    prompt = """
      (S)earch (default when pressing Enter)
      (1-15) Show answers for question number ...
      (N)ext answer
      (L)ist questions again for last search
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
        if choice == '': choice = 's' # hitting Enter = new search
        print '\nYou picked: [%s]' % choice 
        if not choice.isdigit() and choice not in 'snlq':
          print "This is an invalid option, try again"
        else:
          chosen = True
      if choice.isdigit() : self.show_question_answer(int(choice))
      if choice == 's': self.search_questions() 
      if choice == 'n': self.show_more_answers() 
      if choice == 'l': self.list_questions(True) 
      if choice == 'q': sys.exit("Goodbye!")


  def search_questions(self):
    """ Searches stackoverflow for questions containing the search term """
    self.questions = {} 
    self.searchTerm = raw_input("Enter search: ").strip().lower()
    data = {'q': self.searchTerm }
    data = urllib.urlencode(data)
    soup = self.get_url("http://stackoverflow.com/search", data)
    for i,res in enumerate(soup.find_all(attrs={'class': 'result-link'})):
      q = res.find('a')
      self.questions[i+1] = {}
      self.questions[i+1]['url'] = "http://stackoverflow.com" + q.get('href')
      self.questions[i+1]['title'] = q.get('title')
    self.list_questions()


  def get_url(self, url, data=False):
    """ Imports url data into Soup for easy html parsing """
    u = urllib2.urlopen(url, data) if data else urllib2.urlopen(url)
    return Soup(u)


  def list_questions(self, repeat=False):
    """ Lists the questions that were found with the last search action """
    if not self.questions:
      print "No questions found for search <%s>" % self.searchTerm
      return False
    if not self.questions and repeat:
      print "There are no questions in memory yet, please perform a (S)earch first"
      return False
    print "Questions found for search <%s>" % self.searchTerm 
    for q in self.questions:
      print "%d) %s" % (q, self.questions[q]["title"])


  def show_question_answer(self, num):
    """ Shows the question and the first self.showNumAnswers answers """
    entries = []
    if num not in self.questions: 
      print "num <%s> does not appear in questions dict" % str(num) 
      return False
    print "Q&A for %d) %s \n%s\n" % \
      (num, self.questions[num]['title'], self.questions[num]['url'])
    soup = self.get_url(self.questions[num]['url'])
    for i,answer in enumerate(soup.find_all(attrs={'class': 'post-text'})):
      qa = "Question" if i == 0 else "Answer #%d" % i
      out = "%s\n[ %s ]\n%s\n" % ("-"*40, qa, "-"*40)
      out += ''.join(answer.findAll(text=True))
      # print the Q and first Answer, save subsequent answers for iteration with option (N)ext answer
      if i <= self.showNumAnswers:
        print out
      else:
        entries.append(out) 
    self.output = iter(entries)
   

  def show_more_answers(self):
    """ Result of option (N)ext answer: iterates over the next answer (1 per method call) """ 
    if not self.output:
      print "There is no QA output yet, please select a Question listed or perform a (S)earch first"
      return False
    try:
      print self.output.next()
    except StopIteration as e:
      print "All answers shown, choose a question of previous search (L) or press Enter (or S) for a new search"

   
# instant
so = StackoverflowCliSearch()
