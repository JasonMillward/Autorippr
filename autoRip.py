#!/usr/bin/python
#
# MakeMKV Auto Ripper
#
# Uses MakeMKV to watch for movies inserted into DVD/BD Drives
# Looks up movie title on IMDb for saving into seperate directory
#
# Automaticly checks for existing directory/movie and will NOT overwrite
#   existing files or folders
# Checks minimum length of video to ensure movie is ripped not previews or other
#   junk that happens to be on the DVD
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
#   CONSTANTS
#

# Path where the movies are stored
MKV_SAVE_PATH = "/Movies/"

# Minimum Length of video stream in minutes
MKV_MIN_LENGTH = 4800

# MakeMKV Cache
MKV_CACHE = 1024


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
commands.getstatusoutput('makemkvcon -r info > /tmp/makemkv_output')

# Open the info file from /tmp/
tempFile = open('/tmp/makemkv_output', 'r')

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

movieName = movieName.replace("\"", "").replace("_", " ")

sm = imdbScaper.search_movie(movieName, results=5)


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

commands.getstatusoutput(
    'makemkvcon mkv disc:%s 0 "/Movies/%s" ',
    '--cache=1024 --noscan --minlength=4800'
    %
    (discIndex, movieName))

b = datetime.datetime.now()
c = b - a

minutes = c.seconds / 60
print "It took %s minutes to complete the ripping of %s" % (minutes, movieName)
