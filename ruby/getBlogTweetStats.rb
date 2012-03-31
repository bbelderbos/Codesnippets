#!/usr/bin/env ruby
# copyright (c) 2012 Bob Belderbos
# created: January 2012 
require 'net/http'
require 'uri'
require 'rexml/document'
require 'json' 
require 'pp'

urlXml = 'http://bobbelderbos.com/sitemap.xml'
url = 'http://api.tweetmeme.com/url_info.json?url='

xml_data = Net::HTTP.get_response(URI.parse(urlXml)).body
doc = REXML::Document.new(xml_data)

doc.elements.each('urlset/url/loc')  do |element| 
  url += element.text
  resp = Net::HTTP.get_response(URI.parse(url))
  data = resp.body
  result = JSON.parse(data)
  print "#{result['story']['url']} => #{result['story']['url_count']}\n"
end
