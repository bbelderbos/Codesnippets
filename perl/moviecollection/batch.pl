#!/usr/bin/perl
while(<>){ 
 my $cmd = "perl getMovieData.pl \"$_\""; 
 system($cmd);
}
