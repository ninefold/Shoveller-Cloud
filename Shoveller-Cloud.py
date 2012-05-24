from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from libcloud.storage.types import ContainerDoesNotExistError
from libcloud.storage.drivers.atmos import AtmosError
import libcloud.security
import libcloud.storage
from pprint import pprint
import string
import os
import datetime
import time
import sys
import mimetypes
mimetypes.init()
mimetypes.add_type('text/plain', '.bak', strict=True)
mimetypes.add_type('text/plain', '.php', strict=True)

# Checking that all the arguments were entered on the command line, exiting with a message if not.
def checkstart():
    if len(sys.argv) != 4:
        argumentsnotset = 'One or more arguments were not passed. \nUsage is like so: \nPython Shoveller-Cloud.py access-token.txt shared-secret.txt STARTING-DIRECTORY-PATH datestamp=on'
        print argumentsnotset
        sys.exit(1)	

#Set command line arguments and default variables

# Processing text file to retrieve access token
access_token_file = open(sys.argv[1])
for line in access_token_file:
    access_token = line.rstrip()
access_token_file.close()
#print 'Access Token = ', access_token
# Processing text file to retrieve shared secret
shared_secret_file = open(sys.argv[2]) 
for line in shared_secret_file:
    shared_secret = line.rstrip()
shared_secret_file.close()
#print 'Shared Secret = ', shared_secret
scandir = sys.argv[3]
print 'Processing string for starting directory: ' + scandir
scandir=(string.replace(scandir, "\\", "/"))
#print 'Slashes flipped in starting directory: ' + scandir
#scandir = "/test"
date_stamp_toggle = sys.argv[4]
if (date_stamp_toggle == "datestamp=on"):
    rootstring="O"
    print 'Datestamping is ON'
    datestamp = datetime.date.today().strftime("%d-%B-%Y")
    #print datestamp
    container_name = (datestamp)
else:
    print 'Datestamping is OFF'
    rootstring=''
    datestamp=''
    container_name = ('')

print '\nLogging in...'
#Security Block -- Logging in with our certificates
libcloud.security.VERIFY_SSL_CERT = False
Ninefold = get_driver(Provider.NINEFOLD)
driver = Ninefold(access_token, shared_secret)
# This plays out as driver = Ninefold('YOUR Atmos Access Token HERE', 'YOUR Atmos Shared Secret HERE')

#Fuctions for printing the list of files and folders in cloud storage
def showcloudassets():
    containers = driver.list_containers()
    print '\nList of Containers\n'
    pprint(containers)
    print '\n'

def showlocalassets():
    print ('List of local files that will be uploaded:\n\n')
    for a in allfiles:
        print "file: ", a
    for z in alldirs:
        print "directory: ", z
    print ('\nEnd list of local files.\n')

#Scanning all children of the starting directory
allfiles = [] #store all files found
alldirs = [] #store all directories found
for root,dir,files in os.walk(scandir):	
    if (rootstring=="O"): 
        #Code to convert backslashes to forward slashes
        rootstring=(string.replace(root, "\\", "/"))
        alldirs.append(rootstring)
        try:
            container=driver.get_container(datestamp) #Check for the file's existence in cloud storage
            print "\nBase directory already exists: " + datestamp + " -- skipping."
#            time.sleep(10)
        except ContainerDoesNotExistError:
            container=driver.create_container(datestamp)
            print '\nCreating base directory in cloud storage with name: ' + datestamp
#            time.sleep(10)
    dirlist = [ os.path.join(root,di) for di in dir ]
    for d in dirlist: 
        #Code to convert backslashes to forward slashes
        d=(string.replace(d, "\\", "/"))
        d=(string.replace(d, " ", "_"))
        alldirs.append(d)
        container_name = d
    filelist = [ os.path.join(root,fi) for fi in files ]
    for f in filelist:
        f=(string.replace(f, '\\', '/'))
        allfiles.append(f)
        object_name = f
print "\n"

showlocalassets()

#Upload folders to Cloud Storage
print "\n*** BEGIN UPLOAD PROCESS ***"
print "\n*** CREATING DIRECTORIES IN CLOUD***\n"
for d in alldirs:
    container_name = (datestamp + d)
    try:
        container=driver.get_container(container_name) #Check for the file's existence in cloud storage
        print "\n* Directory already exists (skipping):\n" + datestamp + d
    except ContainerDoesNotExistError:
        print '\n* Creating directory in Cloud Storage: \n'+ datestamp + d
        container = driver.create_container(container_name=container_name)
print "\nFinished creating directories.\n"

#Upload files to Cloud Storage
print "\n*** UPLOADING FILES TO CLOUD ***\n"
for f in allfiles:
    local_path = (f)
    f=(string.replace(f, " ", "_")) # Converting spaces to underscores
    cloud_path = (datestamp + f)
    #print '\nProcessing: ' + f 
    try:
        container=driver.get_container(datestamp + f) #Check for the file's existence in cloud storage
        print "\n* File already exists (skipping):\n" + cloud_path
    except ContainerDoesNotExistError:
        print "\n* Uploading to Cloud Storage: " + cloud_path
        URL = (cloud_path)
        #print "\nSplitting off the file name from: " + URL
        file_name = URL.rsplit('/', 1)[1] # Split off the filename from path
        #print 'RESULTS OF FILENAME SPLIT-OFF: ' + file_name
        path_directory = URL.rpartition('/') # Split off the pathname from path
        #print 'RESULTS OF PATHNAME SPLIT-OFF: ' + path_directory[0]
        #print 'local_path = ' + local_path
        #print 'path_directory[0] = ' + path_directory[0]
        container=driver.get_container(path_directory[0])
        #print 'file_name = ' + file_name
        #Adding a content-type setting
        detected_file_type = mimetypes.guess_type(local_path)
        printable_file_type = detected_file_type[0]
        if printable_file_type == None:
            printable_file_type = 'application/binary'
        extra_settings = {'content_type':printable_file_type}
        try:
            driver.upload_object(local_path,container,file_name,extra=extra_settings)
        except:
            print "*** Unexpected error", sys.exc_info()[0] , " -- retrying. ***"
            #raise
        print '*** Success uploading: ' + file_name

print "\n*** END UPLOAD PROCESS ***\n"

showcloudassets()
