# NAME

callback.cgi - registered at Freesound.org as the callback URI for authority approval/denial.

# SYNOPSIS

At [http://www.freesound.org/apiv2/apply](http://www.freesound.org/apiv2/apply) you can set the "Callback URL" to be this
CGI script.  Inputs will be :

    'state' => 'xyz', 'code' => 'AAAAAAAAAAAAABBBBBBBBCCCC12345' 

Or, if the user denies the OAuth2 request (Deny button) :

    'error' => 'access_denied'

If approved then we get the code in our CGI params as above, and can then
call the [WebService::Freesound](https://metacpan.org/pod/WebService::Freesound)->get\_new\_oauth\_tokens method that gets
the access tokens from this code and encapsulate them.

# ACKNOWLEDGEMENTS

Kirsel : https://www.kirsle.net/blog/entry/simple-perl-uploader-with-progress-bar.

# LICENSE AND COPYRIGHT

Copyright 2016 Andy Cragg.

This program is free software; you can redistribute it and/or modify it
under the terms of the the Artistic License (2.0). You may obtain a
copy of the full license at:

[http://www.perlfoundation.org/artistic\_license\_2\_0](http://www.perlfoundation.org/artistic_license_2_0)
