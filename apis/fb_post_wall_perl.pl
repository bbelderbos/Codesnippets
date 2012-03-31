#!/usr/bin/perl -w
#copyright (c) 2011 bob belderbos
#created: August 2011 
#site: http://bobbelderbos.com/2011/08/facebook-api-post-with-perl-from-cli/
#special thanks: http://qscripts.blogspot.com/2011/02/post-to-your-own-facebook-account-from.html


use strict;
use URI;
use LWP::Simple;
use JSON; # imports encode_json, decode_json, to_json and from_json.

my $access_token = '-----'; # see http://qscripts.blogspot.com/2011/02/post-to-your-own-facebook-account-from.html

sub build_query {
  my $uri = URI->new(shift);
  $uri->query_form(@_);
  return $uri->as_string;
}

while(1) { # infinite loop until you get the right fbID to post your link/message to
	print "Enter 'friends' to find his/her ID, 'likes' to find the page ID, or enter 'skip' if you know this info: ";
	chomp(my $cat = <STDIN>);
	next unless $cat eq 'friends' || $cat eq 'likes' || $cat eq 'skip';
	last if ($cat =~ /skip/i );
	
	print "Enter part of your friend's name or title of the liked page: ";
	chomp(my $friend = <STDIN>);

	my $response = get(build_query('https://graph.facebook.com/me/' .$cat,
	  access_token => $access_token
	));
	my $deserialized = from_json( $response );

	foreach my $e(@{$deserialized->{data}}){
		print $e->{id} . ' - ' . $e->{name} . "\n" if $e->{name} =~ /$friend/i;
	}
	
	print "Found ID of friend/ page you want to post to? ";
	chomp(my $answer = <STDIN>);

	last if ($answer =~ /y(es)?/i );	
}


# here you broke the 'lookup' loop so you know which ID to pick.
# as there might be various candidates, you still have to enter the exact fbID
print "Enter the ID of the page / friend you want to post to: ";
chomp(my $fbID = <STDIN>);

print "Enter the URL you want to send (if only a message, press Enter): ";
chomp(my $link = <STDIN>);

print "Enter a message (if you defined an URL, you can leave this blank by pressing Enter: ";
chomp(my $message = <STDIN>);

my $response = get(build_query('https://graph.facebook.com/'.$fbID.'/feed',
  access_token => $access_token,
  message      => $message,
  link         => $link,
  method       => 'post'
));

print "Feedback post method: $response\n == END == \n";

exit 0;
