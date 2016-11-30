#!/usr/bin/perl -w
use strict;
use CGI ':cgi-lib';
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;
use Template;
my $debug = undef;
use XML::LibXML;
use WebService::Freesound;
$|++;

=pod

=head1 NAME

elementski.cgi - display Freesound.org sample waveform, name, play/stop/pause/, timeline, download/progress etc
in a web page.  Mostly done in javascript, but this provides the base HTML via Toolkit::Template.

=cut

my $VERSION = '0.01';

=head1 SYNOPSIS

Uses WebService::Freesound to get OAuth2 authority to download sample files in a simple webpage.  Ajax calls
are made to call other CGI modules for authority, download, ping and progress counter deletion.

You need to register with Freesound - details in perldoc WebService::Freesound.

CGI input is search text (Freesound.org query) which is sent to Freesound.org and is returns an XML list
of matched samples.  The Toolkit::Template provides links to css and javascript to do the visuals.

Creating a very similar web-page to Freesound.org is not really allowed under their terms and conditions
so use this lot sparingly as examples of what can be done.

Supporting CGI are (ones called by javascript are marked AJAX) :

=over 4

=item * callback.cgi - set at L<https://www.freesound.org/apiv2/apply> to authorise the user to use this app. ie L<http://localhost/cgi-bin/elementski/callback.cgi>

=item * download.cgi - (AJAX) : downloads a Freesound.org sample, updates counter file with progress.

=item * delete_counter.cgi - (AJAX) : deletes the download counter when done.

=item * ping.cgi - (AJAX) : polls the counter file for download progress.

=back

=cut

# Print a header first, so we can bung text on the
# screen anywhere from here.
#
print CGI::header();
warningsToBrowser(1);
my $cgi_query = CGI->new;

# DEBUG
my $parameters = Vars;    # All parameters.
print Data::Dumper->Dump( [$parameters], ["parameters"] ) if ($debug);
# END DEBUG

my %args = (
    client_id     => '<your freessound.org client_id>',
    client_secret => '<your freessound.org client_secret>',
    session_file  => '/var/www/elementski/sessions/freesoundrc',
);
my $freesound = WebService::Freesound->new(%args);

# Get state of OAuth2.  Check authority with Freesound.org
# and send TT a message to display the Freesound.org auth
# page in an iframe.  If expired then call $freesound->check_authority
# which  simply refreshes the tokens and we can carry on.
#
my $get_authorisation = "no";
my $rc = $freesound->check_authority( refresh_if_expired => 1 );

# No auth, expired or not. Tell TT to put up the iframe for
# a go at authorising again.
#
if ( !$rc ) {
    $get_authorisation = $freesound->get_authorization_url();
}

my @sample_rows;
my $text_searched_for = "Nothing yet";

# If search text and auth token, then go do.
#
if ( $cgi_query->param('search_text') ) {

    my $query = $cgi_query->param('search_text');
    $text_searched_for = "$query";

    # Field builder for the Freesound.org text query (no ? required).
    #
    # These are the data that will be returned for the query entered into the
    # text box, in XML. Could be json if you ike that sort of thing.
    #
    my $fields
        = "id,name,filesize,license,type,duration,samplerate,previews,url,images";

    my $response
        = $freesound->query("query=$query&fields=$fields&format=xml");

    # See if this worked and attempt at re-auth if not, ie send TT a
    # request for an iframe.
    #
    unless ( $response->is_success ) {
        $get_authorisation = $freesound->get_authorization_url();
    }

    # Requested XML, don't use XML::Simple these days.
    #
    my $xml_string = $response->content( format => 'xml' );

    my $parser = XML::LibXML->new();
    my $doc    = $parser->parse_string($xml_string);

    foreach my $list_item ( $doc->findnodes('/root/results/list-item') ) {

        my $id          = $list_item->findnodes('./id');
        my $ogg_preview = $list_item->findnodes('./previews/preview-hq-ogg');
        my $waveform    = $list_item->findnodes('./images/waveform_m');
        my $url         = $list_item->findnodes('./url');
        my $name        = $list_item->findnodes('./name');
        my $licence     = $list_item->findnodes('./license');
        my $filesize    = $list_item->findnodes('./filesize');
        my $duration    = $list_item->findnodes('./duration');
        my $samplerate  = $list_item->findnodes('./samplerate');

        # Add to hash for TT.
        #
        my @row = (
            $id->to_literal,       $ogg_preview->to_literal,
            $waveform->to_literal, $url->to_literal,
            $name->to_literal,     $licence->to_literal,
            $filesize->to_literal, $duration->to_literal,
            $samplerate->to_literal,
        );

        push @sample_rows, \@row;
    }
}
print "get_authorisation is " . $get_authorisation . "\n" if $debug;

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Data to be displayed in HTML via variables in TT.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
my $file = 'elementski.html';
my $vars = {
    get_authorisation => $get_authorisation,
    text_searched_for => $text_searched_for,
    sample_rows       => \@sample_rows,
};

my $template = Template->new(
    {

        # Where to find template files.
        #
        INCLUDE_PATH =>
            [ '/var/www/elementski/tt/src', '/var/www/elementski/tt/lib' ],

        # pre-process lib/config to define any extra values
        #
        PRE_PROCESS => 'config',
    }
);

$template->process( $file, $vars )
    || die "Template process failed: ", $template->error(), "\n";

=head1 ACKNOWLEDGEMENTS

Kirsle :  https://www.kirsle.net/blog/entry/simple-perl-uploader-with-progress-bar.
And Freesound.org!

=head1 LICENSE AND COPYRIGHT

Copyright 2016 Andy Cragg.

This program is free software; you can redistribute it and/or modify it
under the terms of the the Artistic License (2.0). You may obtain a
copy of the full license at:

L<http://www.perlfoundation.org/artistic_license_2_0>

=cut

