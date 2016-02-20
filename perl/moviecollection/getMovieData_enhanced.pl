#!perl
use strict;
use warnings;

use DBI;             # SQL quoting hack
use XML::Simple;     # Easy XML handling
use URI::QueryParam; # URL mangling
use LWP::UserAgent;  # Provides the interface to the web

my $movie_name = $ARGV[0] ||
    die "Please provide the movie name as the first argument";

# Build up our request URI                                                                                                                                    
my $uri = URI->new( 'http://www.imdbapi.com' );
$uri->query_param( r => 'XML' );
$uri->query_param( t => $movie_name );

# Get the data
my $response = LWP::UserAgent->new->get( $uri );
die "Couldn't get [$uri]" unless $response->is_success;

# This is the magical list of fields specified in the original, and apparently
# the order in which we need to insert in to the table?
my @fields = qw/
    title year rated released genre director writer actors plot poster runtime
    rating votes imdb
/;

# Parse the XML we received moments ago
my $data = XML::Simple->new->XMLin( $response->content );

my $sql = "INSERT INTO movie_collection VALUES ( NULL, " .
        # Take all of the fields. For each, look it up in the XML data structure,
        # and then quote it properly for a SQL command
        ( join ',', map {
                DBD::_::db->quote( $data->{'movie'}->{$_} || '' )
        } @fields ) .
 
        # Throw in the timestamp
        time() . ');';
 
print $sql . "\n";
