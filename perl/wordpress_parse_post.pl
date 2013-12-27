#!/usr/bin/perl
# copyright (c) bob belderbos
# blog post: http://bobbelderbos.com/2011/08/simple-text-to-html-parser-perl-wordpress/
# usage: parsePost.pl blogpost.txt (generates blogpost.html)

use strict;
use warnings; 
use HTML::Entities;

die "Please provide the blogpost.txt to parse ...\n" unless $ARGV[0]; 
 

my $blogTxtFile = shift @ARGV;
die "Cannot open <$blogTxtFile> ...\n"  unless open POST, "<$blogTxtFile";


my $blogHtmlFile = $blogTxtFile; 
$blogHtmlFile =~ s/(.*)\.txt$/$1\.html/g;
open OUT, ">$blogHtmlFile" or die "Cannot open <$blogHtmlFile> ...\n";


my $parse = 1;  # toggle for code blocks


while(<POST>){

  # COMMENTS IN BLOG POST 

	# skip comments = #! (except she-bangs, detected as #!/.. )
	if(/^#!/ && $_ !~ /#!\/../) {
		next;
	}

	
	# HANDLING CODE BLOCKS

	if(/^CODE/) {
	  print OUT "\n<pre>\n";
		$parse = 0;
		next; 
	}
	if(/^\/CODE/){
	  print OUT "</pre>\n";	  
	  $parse = 1;
		next; 
	}
	# when in code blog, encode all to not conflict with html page and/or
	# php of WP
	if($parse == 0){
    my $line = encode_entities($_);
    $line =~ s/&Acirc;//g;
	  print OUT $line;
	  next;
	}


	
	# PRINTING LITERAL STRINGS AFTER # SIGNS

	# print literal # lines (designed to put it literal html)
	if(/^#/) {
	  s/^#//g; 
	  print OUT $_;
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


	# PRINT PARSED LINE
	print OUT $_;


}

close(OUT);
