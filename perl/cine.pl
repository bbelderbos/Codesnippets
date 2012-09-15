#!/usr/bin/perl -w
# author: bob belderbos
# v0.1 sept 2012
# purpose: send an email with all movies on Spanish TV in the next 24 hours
#          sincroguia.tv has a pretty complete list
#          this script servers best in a daily cronjob
#
use strict; 
use Data::Dumper; 
use LWP::Simple;
use Encode qw(encode decode); # http://perlgeek.de/en/article/encodings-and-unicode

my $enc = 'utf-8'; 
my $output;
my $email = "yourname\@example.com";

my @html = getUrl("http://www.sincroguia.tv/todas-las-peliculas.html");

# movie lines start with hh:mm timestamps
for (grep {/^\d{2}:\d{2}|^<br/} @html){
  # separate days
  if(/^<br/){
    s/<br \/>//g;
    $output .= createHeader($_, "*");
    next;
  }

  # parse movies
  m/(\d{2}:\d{2}) - <a.*?"([^"]+)" href="([^"]+)".*- ([^<]+).*/;
  my ($time, $title, $url, $channel) = ($1, $2, $3, $4);
  $output .= encode($enc, 
    createHeader("$time / $channel / $title") . 
    "$url\n" . 
    getMovieInfo($url) . 
    "\n\n");
}

# send me the generated movielist
sendEmail($email, $output);
  


sub getUrl {
  my $url = shift; 
  my @html = split /<\/?li[> ]/, get($url);
  return @html;
}


sub getMovieInfo {
  my $url = shift; 
  my $info;
  for(getUrl($url)){
    next if(! /column/);
    for my $line (split /<\/?h3[> ]/, $_){
      if($line =~ /Director:|rpretes|Idioma|Nacionalidad|A&ntilde/){
        $line =~ s/.*?strong>(.*)<\/strong>(.*)/$1$2\n/g;        
        $line =~ s/A&ntilde;o/Estreno/g;
        $info .= $line ;
      }
    }
    last; 
  }
  return $info;
}  


sub createHeader {
  my $str = shift; 
  my $delimiter = shift // "=";
  my $width = 70;
  my $output = "\n" . $delimiter x $width . "\n" . $str . "\n" . $delimiter x $width . "\n";
  return $output;
}


sub sendEmail {
  my ($to, $output) = @_;
  my $subject = "Today's movies Spanish TV";
  
  # on mail pipe: http://objectmix.com/perl/380680-sending-email-perl-using-pipe-mailx.html
  open my $pipe, '|-', 'mailx', 
    '-s', $subject, 
    # char issue mailx: http://forums.opensuse.org/english/other-forums/development/programming-scripting/419802-charset-problem-mailx.html
    '-S', 'ttycharset=utf-8', '-S', 'sendcharsets=utf-8', '-S', 'encoding=8bit', 
    $to or die "can't open pipe to mailx: $!\n";
  print $pipe $output;
  close $pipe;
}
