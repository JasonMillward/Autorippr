#!/usr/bin/python

# Import libs
import commands
import os.path
import httplib, urllib
import sys
import datetime
import imdb
import time

# Define path
# Define minlength of movie


# sudo apt-get install python-imdbpy

i = imdb.IMDb()

# Setup some vars
discIndex = ""
movieName = ""

# Execute the info gathering
commands.getstatusoutput('makemkvcon -r info > /tmp/makemkv_output')

# Open the output file
f = open('/tmp/makemkv_output', 'r')

# Check to see if there is a disc in the system
for line in f.readlines():
    if line[:4] == "DRV:":
        if "/dev/" in line:
            drive = line.split(',')
            movieName = drive[5].replace("\"", "").title().replace("Extended_Edition", "")
            discIndex = drive[0].replace("DRV:", "")


# If there was no disc, exit
if len(discIndex) == 0:
    print "No disc"
    sys.exit()

movieName = movieName.replace("_", " ")

sm = i.search_movie(movieName, results=5)


if len(sm) > 0:
    movieName = sm[0]
else:
    print "No matching movie"
    sys.exit()

# We have a movie


if os.path.exists('/Movies/%s' % movieName):
    print "Path exists"
    sys.exit()

os.makedirs('/Movies/%s' % movieName)

a = datetime.datetime.now()

commands.getstatusoutput('makemkvcon mkv disc:%s 0 "/Movies/%s" --cache=1024 --noscan --minlength=4800 > ~/derp' % (discIndex, movieName))

b = datetime.datetime.now()
c = b - a

minutes = c.seconds / 60
print "It took %s minutes to complete the ripping of %s" % (minutes, movieName)
