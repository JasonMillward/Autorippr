#!/usr/bin/python
#
# MakeMKV Auto Ripper
#
# Uses MakeMKV to watch for movies inserted into DVD/BD Drives
# Looks up movie title on IMDb for saving into seperate directory
#
# Automaticly checks for existing directory/movie and will NOT overwrite
#   existing files or folders
# Checks minimum length of video to ensure movie is ripped not previews or
#   other junk that happens to be on the DVD
#
#
# Required for use
#
#   Python (Obviously)
#       * Created using 2.7.3 but should work with similar versions
#
#   MakeMKV
#       * http://makemkv.com/
#
#   IMDbPy
#       * sudo apt-get install python-imdbpy
#
# Can be run with a simple cron, every 5 minutes or so.
# DVD goes in, MakeMKV checks, gets proper DVD name, MakeMKV Rips
# DVD does not get ejected, maybe it will get added to later versions
#
# Released under the MIT license
# Copyright (c) 2012, Jason Millward
#
# @category   misc
# @version    $Id: 1.0, 2012-10-07 12:02:33 CST $;
# @author     Jason Millward <jason@jcode.me>
# @license    http://opensource.org/licenses/MIT
#
# Enough with these comments, on to the code

#
#   CONSTANTS
#

# Path where the movies are stored
MKV_SAVE_PATH = "/Movies/"

# Minimum Length of video stream in minutes
MKV_MIN_LENGTH = 4800

# MakeMKV Cache in megabytes
MKV_CACHE = 1024

# Temp file for info gathering
MKV_TEMP_OUTPUT = "/tmp/makemkv_output"

#
#   IMPORTS
#

import commands
import os.path
import datetime
import imdb
import sys

#
#   CODE
#

# Setup some vars
imdbScaper = imdb.IMDb()
discIndex = ""
movieName = ""

# Execute the info gathering
# Save output into /tmp/ for interpreting 3 or 4 lines later
commands.getstatusoutput('makemkvcon -r info > %s' % MKV_TEMP_OUTPUT)

# Open the info file from /tmp/
tempFile = open(MKV_TEMP_OUTPUT, 'r')

# Check to see if there is a disc in the system
#
# For every line in the output
# If the first 4 characters are DRV:
#   Check to see if a device is specified
#       If so, get the 1st and 6th element of the array
for line in tempFile.readlines():
    if line[:4] == "DRV:":
        if "/dev/" in line:
            drive = line.split(',')
            discIndex = drive[0].replace("DRV:", "")
            movieName = drive[5]


# If there was no disc, exit
if len(discIndex) == 0:
    print "No disc detected"
    sys.exit()

# A little fix for extended editions (eg; Die Hard 4)
movieName = movieName.title().replace("Extended_Edition", "")

# Clean up the disc title so IMDb can identify it easier
movieName = movieName.replace("\"", "").replace("_", " ")

# Get the closest 5 results, do nothing with the other 4
result = imdbScaper.search_movie(movieName, results=5)

# If the returned result is not empty, save it, otherwise IMDb can't
#   identify the DVD
if len(result) > 0:
    movieName = result[0]
else:
    print "Can not match movie title with IMDb"
    sys.exit()

# Check to see if the movie is already save in the movie directory
if os.path.exists('%s/%s' % MKV_SAVE_PATH, movieName):
    print "Movie folder already exists, will not overwrite."
    sys.exit()

# The movie directory doesn't exist.

# Create directory
os.makedirs('%s/%s' % MKV_SAVE_PATH, movieName)

# Display some status text for the user
print " "
print "Starting MakeMKV ripping process"

# Get the time MakeMKV started
startTime = datetime.datetime.now()

# Start the making of the mkv
commands.getstatusoutput(
    'makemkvcon mkv disc:%s 0 "%s/%s" ',
    '--cache=%d --noscan --minlength=%d'
    %
    (discIndex, MKV_SAVE_PATH, movieName, MKV_CACHE, MKV_MIN_LENGTH))

# Get the time MakeMKV finished
endTime = datetime.datetime.now()

# Do some maths here
totalTime = endTime - startTime

# Convert the time into seconds, then turn it into minutes
minutes = totalTime.seconds / 60

# And... we're done. Show some final status messages
print "MakeMKV ripping process completed"
print " "
print "It took %s minutes to complete the ripping of %s" % (minutes, movieName)
