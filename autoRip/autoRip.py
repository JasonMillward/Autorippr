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
#   IMPORTS
#

import os
import datetime
import sys
import ConfigParser
from ripper import makeMKV
#
#   CONFIG VARIABLES
#
REAL_PATH = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.RawConfigParser()
config.read('%s/../settings.cfg' % REAL_PATH)


MKV_SAVE_PATH = config.get('MKV_RIP', 'save_path')
MKV_MIN_LENGTH = config.getint('MKV_RIP', 'min_length')
MKV_CACHE_SIZE = config.getint('MKV_RIP', 'cache_MB')
MKV_TEMP_OUTPUT = config.get('MKV_RIP', 'temp_output')

#
#   CODE
#

MKVapi = makeMKV(MKV_TEMP_OUTPUT)

# Find the disc or exit
if (MKVapi.findDisc() == False):
    # No disc
    sys.exit()

# Get the title
movieTitle = MKVapi.getTitle()

# Check to see if the movie is already save in the movie directory
if os.path.exists('%s/%s' % (MKV_SAVE_PATH, movieTitle)):
    print "Movie folder already exists, will not overwrite."
    sys.exit()

# The movie directory doesn't exist.
# Create a new directory for the movie
os.makedirs('%s/%s' % (MKV_SAVE_PATH, movieTitle))

# Display some status text for the user
print " "
print "Starting MakeMKV ripping process"

# Get the time MakeMKV started
startTime = datetime.datetime.now()

MKVapi.ripDisc(path=MKV_SAVE_PATH, length=MKV_MIN_LENGTH, cache=MKV_CACHE_SIZE)

# Get the time MakeMKV finished
endTime = datetime.datetime.now()

# Do some maths here
totalTime = endTime - startTime

# Convert the time into seconds, then turn it into minutes
minutes = totalTime.seconds / 60

# And... we're done. Show some final status messages
print "MakeMKV ripping process completed"
print " "
print "It took %s minutes to complete the ripping of %s" % (minutes, movieTitle)
