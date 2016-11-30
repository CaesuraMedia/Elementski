#!/usr/bin/perl -w
use strict;
use CGI ':cgi-lib';
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;
my $debug = 1;
use WebService::Freesound;
$|++;

=pod

=head1 NAME

callback.cgi - registered at Freesound.org as the callback URI for authority approval/denial.

=cut

my $VERSION = '0.01';

=head1 SYNOPSIS

At L<http://www.freesound.org/apiv2/apply> you can set the "Callback URL" to be this
CGI script.  Inputs will be :

    'state' => 'xyz', 'code' => 'AAAAAAAAAAAAABBBBBBBBCCCC12345' 

Or, if the user denies the OAuth2 request (Deny button) :

    'error' => 'access_denied'

If approved then we get the code in our CGI params as above, and can then
call the L<WebService::Freesound>->get_new_oauth_tokens method that gets
the access tokens from this code and encapsulate them.

=cut

my %args = (
    client_id     => '<your freessound.org client_id>',
    client_secret => '<your freessound.org client_secret>',
    session_file  => '/var/www/elementski/sessions/freesoundrc',
);

my $freesound = WebService::Freesound->new(%args);

# Print a header first, so we can bung text on the
# screen anywhere from here.
#
print CGI::header();
warningsToBrowser(1);
my $cgi_query = CGI->new;

# Should have  from Freesound.org.
#
# $parameters = { 'state' => 'xyz', 'code' => 'HXFixtbWGKI4asbvymrzWSzsquiLZi' };
# Or :
# $parameters = { 'error' => 'access_denied' };
#
# Prints are in the iFrame.
#
if ( $cgi_query->param('code') ) {

    my $rc = $freesound->get_new_oauth_tokens( $cgi_query->param('code') );
    if ($rc) {
        print "<p>Authorisation ok, now use the search box</p>";
    }
    else {
        print "<p>" . $freesound->error . "</p>";
    }

}
elsif ( $cgi_query->param('error') ) {
    print "<p>"
        . $cgi_query->param('error')
        . " : refresh page to try again.</p>";
}
else {
    print "<p>Not Authorised</p>";
}

=head1 ACKNOWLEDGEMENTS

Kirsel : https://www.kirsle.net/blog/entry/simple-perl-uploader-with-progress-bar.

=head1 LICENSE AND COPYRIGHT

Copyright 2016 Andy Cragg.

This program is free software; you can redistribute it and/or modify it
under the terms of the the Artistic License (2.0). You may obtain a
copy of the full license at:

L<http://www.perlfoundation.org/artistic_license_2_0>

=cut

