#!/usr/bin/perl
# copyright (c) bob belderbos
# blog post: http://bobbelderbos.com/2011/08/simple-text-to-html-parser-perl-wordpress/

use strict;
use warnings; 

die "Please specify your marked up blog text file ...\n" unless $ARGV[0]; 
 
my $file = shift @ARGV;
my $parse = 1;  # toggle for code blocks

die "Cannot open file <$file> ...\n"  unless open POST, '<', $file;

while(<POST>){

  # COMMENTS IN BLOG POST 

	# skip comments = #! (except she-bangs, detected as #!/.. )
	if(/^#!/ && $_ !~ /#!\/../) {
		next;
	}


	
	# HANDLING CODE BLOCKS

	if(/^CODE/) {
	  print "\n<pre>\n";
		$parse = 0;
		next; 
	}
	if(/^\/CODE/){
	  print "</pre>\n";	  
	  $parse = 1;
		next; 
	}
	# when in code blog, print everything literally as stated
	if($parse == 0){
	  print;
	  next;
	}


	
	# PRINTING LITERAL STRINGS AFTER # SIGNS

	# print literal # lines (designed to put it literal html)
	if(/^#/) {
		s/#//g; 
	  print;
	  next;
	}


  # FB LIKE BUTTON

	s/^LIKE/<fb:like href="" send="true" width="580" show_faces="false" action="like" font=""><\/fb:like>/g;


	
	# OTHER MARKUP
	
	# teaser and headers
	s/^MORE$/<!--more-->/g;			#intro text delimiter
	s/^>>>>\s?(.*?)$/<h4>$1<\/h4>/g; 	#h4 subheaders (before h3 = >>> !)
	s/^>>>\s?(.*?)$/<h3>$1<\/h3>/g; 	#h3 headers
	
	# links (marked up as : ||name||<a href..)
	# how to distinguish dot in url from real dot in text ? 
	s/\|\|([^\|]*)\|\|(https?:\/\/\S+)\s/<a href="$2" target="_blank">$1<\/a>/g;		
	
	# images (marked up as : !alt tag!!link!!float!!width)	
	s/!!(.*?)!!(http:\/\/[^\s!]+)!!(left|right|none)!!(\d{3})/<img class="size-full" src="$2" alt="$1" style="float:$3; margin: 20px;" width="$4">/g;
	
	# normal paragraphs
	s/^::(.*?)\s?$/<p>$1<\/p>/g; 
	
	# ul li blocks
  s/^-(.*)/<li>$1<\/li>/g;
  s/^\*{2}/<\/ul>/g;
  s/^\*/<ul>/g;


  # PRINT RESULT

  print;


}
