#!/usr/bin/perl -w
use strict;
use LWP::Simple;
use LWP::UserAgent;
use CGI;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use WebService::Freesound;
use Carp;
$|++;
print CGI::header();
warningsToBrowser(1);
fatalsToBrowser(1);

=pod

=head1 NAME

download.cgi - downloads a sample from Freesound.org as a callback from a javascript Ajax call.

=cut

my $VERSION = '0.01';

=head1 SYNOPSIS

Downloads the Freesound.org sample to web-writable directory, writing
the counter file for progress ($freesound->download does this).  If 
the authority has expred or been revoked then the counter file has 
"auth_error:auth_error:auth_error" in it for javascript to pick up 
and display a re-auth message.

=cut

my %args = (
    client_id     => '<your freessound.org client_id>',
    client_secret => '<your freessound.org client_secret>',
    session_file  => '/var/www/elementski/sessions/freesoundrc',
);
my $freesound = WebService::Freesound->new(%args);

my $query = CGI->new;
if ( $query->param('id') ) {

    my $id           = $query->param('id');
    my $counter_file = "/var/www/elementski/downloads/counter_$id.txt";
    my $freesound    = WebService::Freesound->new(%args);
    my $rc           = $freesound->check_authority;
    if ( !$rc ) {
        open my $fh, '>', $counter_file
            or croak "Cannot read provided counter_file for writing : $!";
        print $fh "auth_error:auth_error:auth_error";
        close $fh;
        exit;
    }

    my $file = $freesound->download( $id, '/var/www/elementski/downloads/',
        $counter_file );

}
else {
    print "CGI error - no Freesound id given for downloading";
}

=head1 ACKNOWLEDGEMENTS

Kirsle :  https://www.kirsle.net/blog/entry/simple-perl-uploader-with-progress-bar.

=head1 LICENSE AND COPYRIGHT

Copyright 2016 Andy Cragg.

This program is free software; you can redistribute it and/or modify it
under the terms of the the Artistic License (2.0). You may obtain a
copy of the full license at:

L<http://www.perlfoundation.org/artistic_license_2_0>

=cut

