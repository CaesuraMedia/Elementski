# NAME

elementski.cgi - display Freesound.org sample waveform, name, play/stop/pause/, timeline, download/progress etc
in a web page.  Mostly done in javascript, but this provides the base HTML via Toolkit::Template.

# SYNOPSIS

Uses WebService::Freesound to get OAuth2 authority to download sample files in a simple webpage.  Ajax calls
are made to call other CGI modules for authority, download, ping and progress counter deletion.

You need to register with Freesound - details in perldoc WebService::Freesound.

CGI input is search text (Freesound.org query) which is sent to Freesound.org and is returns an XML list
of matched samples.  The Toolkit::Template provides links to css and javascript to do the visuals.

Creating a very similar web-page to Freesound.org is not really allowed under their terms and conditions
so use this lot sparingly as examples of what can be done.

Supporting CGI are (ones called by javascript are marked AJAX) :

- callback.cgi - set at [https://www.freesound.org/apiv2/apply](https://www.freesound.org/apiv2/apply) to authorise the user to use this app. ie [http://localhost/cgi-bin/elementski/callback.cgi](http://localhost/cgi-bin/elementski/callback.cgi)
- download.cgi - (AJAX) : downloads a Freesound.org sample, updates counter file with progress.
- delete\_counter.cgi - (AJAX) : deletes the download counter when done.
- ping.cgi - (AJAX) : polls the counter file for download progress.

# ACKNOWLEDGEMENTS

Kirsle :  https://www.kirsle.net/blog/entry/simple-perl-uploader-with-progress-bar.
And Freesound.org!

# LICENSE AND COPYRIGHT

Copyright 2016 Andy Cragg.

This program is free software; you can redistribute it and/or modify it
under the terms of the the Artistic License (2.0). You may obtain a
copy of the full license at:

[http://www.perlfoundation.org/artistic\_license\_2\_0](http://www.perlfoundation.org/artistic_license_2_0)
