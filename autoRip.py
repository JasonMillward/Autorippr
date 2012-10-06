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
# Released under the MIT license
#
# @copyright  2012 jCode
# @category   misc
# @version    $Id$
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

# MakeMKV Cache
MKV_CACHE = 1024

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
            movieName = drive[5].title().replace("Extended_Edition", "")


# If there was no disc, exit
if len(discIndex) == 0:
    print "No disc"
    sys.exit()

# Clean up the disc title so IMDb can identify it easier
movieName = movieName.replace("\"", "").replace("_", " ")

# Get the closest 5 results, do nothing with the other 4
result = imdbScaper.search_movie(movieName, results=5)

# If the returned result is not empty, save it, otherwise IMDb can't
#   identify the DVD
if len(result) > 0:
    movieName = result[0]
else:
    print "No matching movie"
    sys.exit()


if os.path.exists('/Movies/%s' % movieName):
    print "Path exists"
    sys.exit()

os.makedirs('/Movies/%s' % movieName)

a = datetime.datetime.now()

commands.getstatusoutput(
    'makemkvcon mkv disc:%s 0 "/Movies/%s" ',
    '--cache=1024 --noscan --minlength=4800'
    %
    (discIndex, movieName))

b = datetime.datetime.now()
c = b - a

minutes = c.seconds / 60
print "It took %s minutes to complete the ripping of %s" % (minutes, movieName)
