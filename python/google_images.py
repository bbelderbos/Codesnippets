# modified version from https://developers.google.com/image-search/v1/jsondevguide
import urllib, urllib2, simplejson, socket, sys, pprint
if(len(sys.argv) < 2):
  sys.exit("please aprovide search string")
else:
  search = urllib.quote_plus(sys.argv[1])

ip = socket.gethostbyname(socket.gethostname())
size = "imgsz=small|medium|large|xlarge"
results = "rsz=8"
url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
       'v=1.0&q=%s&userip=%s&as_filetype=png&%s&%s' % (search, ip, size, results))
print url

request = urllib2.Request(url, None, {'Referer': 'http://bobbelderbos.com' })
response = urllib2.urlopen(request)

# Process the JSON string.
results = simplejson.load(response)
pprint.pprint(results)
