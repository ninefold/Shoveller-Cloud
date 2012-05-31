Shoveller Cloud

A Python script for uploading a large directory tree (with all files) to cloud storage. 

Requires the Python 2.7.3 runtime:
http://python.org/download/releases/2.7.3/

...and the apache Libcloud library:
http://libcloud.apache.org/

By Ed Dawson (edwin.dawson@gmail.com), @TheRealEdDawson

Licensed under the GPL 2.0 (GNU General Public License, Version 2)

Known issues: 
 * The specified starting folder must not have spaces in its name.
 * Any subfolders with spaces in the name will have the spaces converted to underscores on cloud storage. 
 * Files with a file size of zero bytes will not be uploaded.

