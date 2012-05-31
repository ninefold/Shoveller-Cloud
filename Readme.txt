Shoveller Cloud

A Python script for uploading files to cloud storage. 

By Ed Dawson (edwin.dawson@gmail.com), @TheRealEdDawson

Requires the Python 2.7.3 runtime:
http://python.org/download/releases/2.7.3/

...and the apache Libcloud library:
http://libcloud.apache.org/

Licensed under the GPL 2.0 (GNU General Public License, Version 2)

Known issues: 
 * The specified starting folder must not have spaces in its name.
 * Any subfolders with spaces in the name will have the spaces converted to underscores. 
 * Files with a file size of zero bytes will not be uploaded.

