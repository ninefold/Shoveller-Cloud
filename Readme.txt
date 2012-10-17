Shoveller Cloud

A Python script for uploading a large directory tree (with all files) to Ninefold cloud storage. 

Requires the Python 2.7.3 runtime:
http://python.org/download/releases/2.7.3/

...and the apache Libcloud library:
http://libcloud.apache.org/

Shoveller-Cloud Installation

1. Requires the Python 2.7.3 runtime: http://python.org/download/releases/2.7.3/
2. Also requires the Apache Libcloud library: http://libcloud.apache.org/ To install Libcloud, use: "pip install apache-libcloud" 
under Linux. 
On Windows you will need to download and install the Libcloud binaries (place the /libcloud/ directory under /Python27/Lib/).
3. Download the Shoveller-Cloud project from Github: https://github.com/ninefold/Shoveller-Cloud/zipball/master
Unpack the zip file into a folder on your local machine.
4. Create two text files in the same folder as the Shoveller-Cloud.py file. Call them access-token.txt and shared-secret.txt.
5. Retrieve your cloud account’s access token and shared secret keys. On Ninefold, these are visible in the portal. 
Log into the Ninefold portal and click Summary > View Cloud Storage Keys. The ones you want are the “Atmos Access Token” 
and the “Amos Shared Secret”. Copy and paste the key for the Atmos Access Token into access-token.txt and the Atmos Shared 
Secret into shared-secret.txt and save them.
6. Launch the script from the command prompt / shell, with the following: 
python Shoveller-Cloud.py access-token.txt shared-secret.txt /yourdir/ datestamp=on
(where /yourdir/ is the directory you want to upload from the local machine).
Note: the “datestamp” option, when switched on, will create a root folder in cloud storage with today’s date. 
This can be helpful if you want to upload the same directory tree a number of times and keep separate versions of it. 
The starting directory you select must not have any spaces in its name.

By Ed Dawson (edwin.dawson@gmail.com), @TheRealEdDawson

Licensed under the GPL 2.0 (GNU General Public License, Version 2)

Known issues: 
 * The specified starting folder must not have spaces in its name.
 * Any subfolders with spaces in the name will have the spaces converted to underscores on cloud storage. 
 * Files with a file size of zero bytes will not be uploaded.

