#!/usr/bin/perl -w
#copyright (c) 2011 bob belderbos
#created: 1st Oct 2011 
#mentioned: http://bobbelderbos.com/2011/08/simple-text-to-html-parser-perl-wordpress/ 

use strict; 
use Data::Dumper; 
use JSON;
use LWP::Simple;
use Getopt::Std; 

my %opts;
getopts('jst', \%opts);  # (j)ason or (s)ql or (t)ext
die "Usage: perl -w parseCategories.pl -j -s, where -j = json, -s = sql, -t = text" 
	unless (defined $opts{j} || defined $opts{s} || defined $opts{t}) ;

my $url = 'http://www.thealternativebookshop.com/category.html';
my $content = get $url;
die "Couldn't get $url" unless defined $content;

my @fileContents = split (/\n/,$content);
#print Dumper(@fileContents); exit;

my %subCategories; # store endresult list
my $cat; # tmp variable to hold cat
my $subCat; # tmp variable to hold cat->subcat
my $id = 0;

foreach my $line (@fileContents){
	$_ = $line;
	chomp;
	$id++;	
	if (/<font color.*<ul>/) {
		s/.*strong>(.*)<\/strong.*/$1/g;
		$cat = $_;
	}
	if(/<li><a href=.*<\/a><\/li>/){
		s/\s*<li><a href=".*">(.*)<\/a><\/li>/$1/g;
		$subCat = "$cat | $_";
		$subCategories{$id} = $subCat;
	}	
}

if($opts{j}) {
	my $json_text = to_json(\%subCategories);
	print $json_text;
} elsif($opts{s}) {
	my $sqlIns;
	foreach my $val (values %subCategories) { $sqlIns .= "\nINSERT INTO book_categories (category) VALUES ('$val');\n"; }
	print $sqlIns;
} elsif($opts{t}) {
	foreach my $val (values %subCategories) { print "$val\n" };
}
