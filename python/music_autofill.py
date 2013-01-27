#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/8948/accessing-mp3-meta-data-with-python
import os, fnmatch, sys, optparse, random, shutil, json
import eyed3 # probably the only module you have to install for a modern python - http://eyed3.nicfit.net 

class MusicAutofill(object):
  """ Trying to simulate itunes autofill feature to get random music from a specified music library to a remote directory, 
      ideal for an USB device in the car for example (motivation). There are various command line switches, you need to 
      provide the music library path, and the destination path to copy the songs to. You also need to specify the max. size
      of the autofill in MB. Optional switches are genres, so you can be more specific what music you want, you also can specify
      a max length in minutes for each song, to avoid longer songs filling up your device. At last I found one bottleneck: the time 
      eyed3 took for a large music library, that's why I put caching in dumping the library details to json. This way you only 
      have to run it for some time the first time, and the next time (specifying the -c option) you can use the cached json ...
      Enjoy! """

  def __init__(self):
    """ When instantiating this class, process cli args, and get mp3 file data, cache data if specified from cli """
    opts = self.parse_cli()
    self.musicLib = opts.path
    self.autoFillDestination = opts.usb
    self.maxAutofillSizeBytes = int(opts.size) * 1024 * 1024 # given in MB 
    self.filterOnGenres = self.select_genres() if opts.genres else False 
    self.maxSongLengthSeconds = int(opts.length) * 60 if opts.length else False 
    self.verbose = opts.verbose
    self.cache = opts.cache
    self.mp3Files = self.list_mp3_files()
    if self.cache: self.cacheFile = self.musicLib + os.sep + "my_music_library.json"
    self.mp3FileDetails = self.get_mp3_data()
    if self.cache: self.cache_outputs()


  def parse_cli(self):
    """ CLI option parsing """
    parser = optparse.OptionParser()
    # mandatory
    parser.add_option('-p', '--path', help='path to music lib', dest='path')
    parser.add_option('-u', '--usb', help='path to usb stick', dest='usb')
    parser.add_option('-s', '--size', help='max size autofill in MB', dest='size')
    # optional, recommended is -c if you have a big music library
    parser.add_option("-g", "--genres", help='filter on genres', dest='genres', action='store_true', default=False)
    parser.add_option("-l", "--length", help='max length of song in minutes', dest='length', default=False) # rfe: support also > duration
    parser.add_option("-v", "--verbose", help='verbose switch', dest='verbose', action='store_true', default=False)
    parser.add_option("-c", "--caching", help='dump music lib to json for fast retrieval', dest='cache', action='store_true', default=False)
    (opts, args) = parser.parse_args()
    # Making sure all mandatory options appeared.
    mandatories = ['path', 'usb', 'size']
    for m in mandatories:
      if not opts.__dict__[m]:
        print "Mandatory option is missing: [%s]\n" % m
        parser.print_help()
        exit(-1)
    # validate paths
    for dirName in [opts.path, opts.usb]:
      self.path_exists_check(dirName)
    return opts


  def path_exists_check(self, dirName):
    """ Exit if musicLib and destination (USB) path don't exist """
    if not os.path.isdir(dirName):
      sys.exit("%s does not exist" % dirName)


  def select_genres(self):
    """ If -g is given, user is prompted to enter genres to make autofill more specific """
    userInput = raw_input("provide genres to filter on, seperated by commas: ")
    return [genre.lower() for genre in userInput.split(", ")]


  def list_mp3_files(self):
    """ Recursively walk through given musicLib dir, listing all mp3 files """
    # http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
    mp3Files = []
    for root, dirnames, filenames in os.walk(self.musicLib):
      for filename in fnmatch.filter(filenames, '*.mp3'):
        mp3Files.append(os.path.join(root, filename))
    if self.verbose: print "%s files found in %s" % (len(mp3Files), self.musicLib)
    return mp3Files


  def get_mp3_data(self):
    """ Use eyed3 to get relevant mp3 metadata """
    if self.cache and os.path.isfile(self.cacheFile):
      mp3FileDetails = self.retrieve_cached_output()
    else:
      mp3FileDetails = {}
      for mp3 in self.mp3Files: 
        try:
          a = eyed3.load(mp3)
        except:
          print "error when getting metadata of %s" % mp3
          continue
        try:
          mp3FileDetails[mp3] = {}
          # !! tricky to get the below 3 attributes, they sometimes are not available for good songs
          #    and the info is in the filename anyways , leaving them here for documentation of eyed3
          #mp3FileDetails[mp3]['title'] = a.tag.title  
          #mp3FileDetails[mp3]['album'] = a.tag.album 
          #mp3FileDetails[mp3]['artist'] = a.tag.artist 
          mp3FileDetails[mp3]['bytes'] = a.info.size_bytes 
          mp3FileDetails[mp3]['seconds'] = a.info.time_secs
          mp3FileDetails[mp3]['genre'] = a.tag.genre.name 
        except AttributeError as e:
          # cannot continue without details
          # - bytes is necessary to calculate maxAutofillSizeBytes
          # - seconds is needed if user chooses max length of song
          # - genre is needed if user chooses genre to filter on
          if self.verbose: 
            print "cannot get details for %s (%s)" % (mp3, e)
            print "to debug, run $ eyeD3 '%s'" % mp3
          continue
      if self.verbose: print "mp3 data found for %s files" % len(mp3FileDetails)
    return mp3FileDetails


  def cache_outputs(self):
    """ If caching is active (-c option) dump music lib to json """ 
    # http://stackoverflow.com/questions/7100125/storing-python-dictionaries
    try: 
      with open(self.cacheFile, 'wb') as fp:
        json.dump(self.mp3FileDetails, fp)
    except IOError as e:
      print "Unable to cache music library (%s)" % e

  
  def retrieve_cached_output(self):
    """ If caching is active (-c option) retrieve music lib json dump """
    if self.verbose: print "retrieving mp3file details from cached json file: %s" % self.cacheFile
    try:
      with open(self.cacheFile, 'rb') as fp:
        return json.load(fp)
    except IOError as e:
      print "Unable to retrieve music library (%s)" % e


  def auto_fill(self):
    """ The workhorse that fills the destination path (usb) with music based on provided criteria """
    sizeFilled = 0
    successCounter = failureCounter = 0
    songsTaken = []
    while sizeFilled < self.maxAutofillSizeBytes: 
      # take a random song from collection
      randomSong = random.choice(self.mp3FileDetails.keys())
      # don't take a song twice
      if randomSong in songsTaken:
        continue
      songsTaken.append(randomSong)
      # if genres have been given in args, filter
      if self.filterOnGenres:
        if not "genre" in self.mp3FileDetails[randomSong] or self.mp3FileDetails[randomSong]['genre'].lower() not in self.filterOnGenres:
          continue
      # if user specified max size of songs:
      if self.maxSongLengthSeconds:
        if not "seconds" in self.mp3FileDetails[randomSong] or self.mp3FileDetails[randomSong]['seconds'] > self.maxSongLengthSeconds:
          continue
      copySuccess = self.copy_mp3_to_usb(randomSong)
      if copySuccess:
        successCounter += 1
      else: 
        failureCounter += 1
      sizeFilled += self.mp3FileDetails[randomSong]['bytes']
    print "%s bytes reached, we're done!" % self.maxAutofillSizeBytes
    print "Successfully copied: %s / failures upon copying: %s" % (successCounter, failureCounter)
    if self.cache:  
      print "Cache file %s was used" % self.cacheFile
      print "- to run without caching, don't use the -c option"
      print "- to refresh the cache, delete the mentioned file"


  def copy_mp3_to_usb(self, mp3ToCopy):
    """ Copies speficied mp3 file to autofill location/path, returns True/False if success/failure """
    destinationFile = self.autoFillDestination + os.sep + os.path.basename(mp3ToCopy)
    if self.verbose: 
      print "file to copy: %s" % mp3ToCopy
      print "destination full path : %s" % destinationFile
      print "-----\n"
    try:
      shutil.copyfile(mp3ToCopy, destinationFile)
      return True
    except IOError as e:
      if self.verbose: print "problem copy: %s" % e
      return False


# instant
m = MusicAutofill()
m.auto_fill()
