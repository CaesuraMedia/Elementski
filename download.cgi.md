# NAME

download.cgi - downloads a sample from Freesound.org as a callback from a javascript Ajax call.

# SYNOPSIS

Downloads the Freesound.org sample to web-writable directory, writing
the counter file for progress ($freesound->download does this).  If 
the authority has expred or been revoked then the counter file has 
"auth\_error:auth\_error:auth\_error" in it for javascript to pick up 
and display a re-auth message.

# ACKNOWLEDGEMENTS

Kirsle :  https://www.kirsle.net/blog/entry/simple-perl-uploader-with-progress-bar.

# LICENSE AND COPYRIGHT

Copyright 2016 Andy Cragg.

This program is free software; you can redistribute it and/or modify it
under the terms of the the Artistic License (2.0). You may obtain a
copy of the full license at:

[http://www.perlfoundation.org/artistic\_license\_2\_0](http://www.perlfoundation.org/artistic_license_2_0)
