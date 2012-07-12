#!/usr/bin/perl -w
#copyright (c) 2011 bob belderbos
#created: August 2011 
#site: http://bobbelderbos.com/2011/08/facebook-api-post-with-perl-from-cli/
#script is edited version of: http://qscripts.blogspot.com/2011/02/post-to-your-own-facebook-account
-from.html

use 5.008_004;
use strict;
use URI;
use LWP::Simple;
use JSON; # imports encode_json, decode_json, to_json and from_json.

# get your token from http://www.bobbelderbos.com/fbwall/
my $access_token = '----'; 

sub build_query {
  my $uri = URI->new(shift);
  $uri->query_form(@_);
  return $uri->as_string;
}

(@ARGV > 0) or die "at least provide a message from command line\n Usage: postMe.pl <req message> <o
pt url> <opt img>";
my $message = $ARGV[0];
my $link = (defined $ARGV[1])? $ARGV[1] : '' ;

my $response = get(build_query('https://graph.facebook.com/me/feed',
  access_token => $access_token,
  message      => $message,
  link         => $link,
  method       => 'post'
)) or die "Something went wrong: could not post to wall\n";

$response =~ s/\{"id":"(.*)"\}/$1/g; 
print "Post in graph: http://graph.facebook.com/$response\n";

exit 0;