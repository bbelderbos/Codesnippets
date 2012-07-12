#!/usr/bin/perl -w
# author: bob belderbos july 2012
# purpose: copy a photos from Pictures to an album folder, 
# based on a provided list of photo numbers

use strict; 
use Data::Dumper; 
use File::Copy;


my $albumName = shift or die usage(); 
my $inputFile = shift or die usage(); 

my $pictures_dir = '/Users/bob/Pictures/2012/new/';
if(! -d $pictures_dir) {
	die "$pictures_dir not found so cannot search it for photos, exiting ...\n";
}

my $destination_dir = "/Users/bob/Desktop/tmp/$albumName/";
if(! -d $destination_dir) {
	print "$destination_dir not present, creating it now ... \n";
	mkdir $destination_dir or die "Destination dir could not be created: $!";	
}

my @photos = get_photo_ids($inputFile);
# print Dumper(@photos); exit; 
copy_photos(@photos);



sub usage {
	print "Usage: $0 [album name] [file with photo numbers] (source dir)\n"
}


sub slurp_file {
	my $filename = shift; 
	open my $fh, "<", $filename or die $!;
	local $/; # enable localized slurp mode
	my $content = <$fh>;
	close $fh;
	return $content;
}


sub get_photo_ids {
	my $inputFile = shift; 
	my $content = slurp_file($inputFile) or die "Cannot get content of input file\n";	
	# split on any non-digit character, effectively this gives all numbers in the file
	my @photos = split /\D+/, $content;

	# make sure we do an extra check an only return xx number of digits
	return grep { /\d+/ } @photos;
}


sub copy_photos {
	my $counterOK = 0; my $counterFail = 0;
	my $img_prefix = "IMG_"; my $img_extension = ".JPG";
	my @photos = @_; 

	for my $photo (@photos) {
		my $photoName = $img_prefix.$photo.$img_extension;

		if (copy( $pictures_dir.$photoName  ,  $destination_dir.$photoName )) {
			$counterOK++;
		} else { 
			$counterFail++;
			print "Copy $photoName failed: $!\n";
		}
	}

	print "Job done: $counterOK photos copied successfully, $counterFail photos could not be copied, see output above ...\n";
}
