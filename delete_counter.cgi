#!/usr/bin/perl -w
use strict;
use LWP::Simple;
use LWP::UserAgent;
use CGI;
$|++;
print CGI::header();

=pod

=head1 NAME

delete_counter.cgi - deletes the counter file associated with a sample download progress

=cut

my $VERSION = '0.01';

=head1 SYNOPSIS

Deletes the counter file when called by an Ajax callback routine,
to avoid clogging the system and odd visual effects if the couner
for an already downloaded file is at 100%.

=cut

my $cgi_query = CGI->new;

if ( $cgi_query->param('id') ) {

    my $freesound_id = $cgi_query->param('id');

    my $counter_file
        = "/var/www/elementski/downloads/counter_$freesound_id.txt";
    if ( -f $counter_file ) {
        unlink($counter_file);
        print "Deleted";
    }
    else {
        print "CGI-error, $counter_file not found";
    }
}
else {
    print "CGI-error : no id param";
}

=head1 ACKNOWLEDGEMENTS

Kirsle : https://www.kirsle.net/blog/entry/simple-perl-uploader-with-progress-bar.

=head1 LICENSE AND COPYRIGHT

Copyright 2016 Andy Cragg.

This program is free software; you can redistribute it and/or modify it
under the terms of the the Artistic License (2.0). You may obtain a
copy of the full license at:

L<http://www.perlfoundation.org/artistic_license_2_0>

=cut

