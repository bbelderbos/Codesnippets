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
my $email = "yourname\@mail.com";

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
  my $info = q{};
  for(getUrl($url)){
    
    if( /column/) {
      for my $line (split /<\/?h3[> ]/, $_){
        if($line =~ /Director:|rpretes|Idioma|Nacionalidad|A&ntilde/){
          $line =~ s/.*?strong>(.*)<\/strong>(.*)/$1$2\n/g;        
          $line =~ s/A&ntilde;o/Estreno/g;
          $info .= $line ;
        }
      }
      $info .= "\n";
    }


    if( /contentficha/ ) {
      my @lines = split /\n/;
      for my $line (@lines) {
        if($line =~ /<h2>|Calificaci/){
          $line =~ s/.*?(<br.*)/$1/g;        # take the img off the summary
          $line =~ s/(\s*<[^>]+?>\s*)+//g;   # take out all html tags
          $line =~ s/\((.*?)\)/ |> $1 <| /g;       # spaces around subtitle
          $info .= "$line\n\n"; 
        }
      }
    }

    # get the links to share this movie on FB and Twitter
    if( /.*(http.*facebook.com[^'"]+\.html).*/ ) {
      m/.*(http.*facebook.com[^'"]+\.html).*(http.*twitter.com\/intent[^'"]+).*/sm;
      $info .= "Share on Facebook: $1\n";
      $info .= "Share on Twitter: $2\n";
    }

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
