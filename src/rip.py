"""
MakeMKV Auto Ripper

Uses MakeMKV to watch for movies inserted into DVD/BD Drives
Looks up movie title on IMDb for saving into seperate directory

Automaticly checks for existing directory/movie and will NOT overwrite existing
files or folders
Checks minimum length of video to ensure movie is ripped not previews or other
junk that happens to be on the DVD


This script can be run with a simple cron, every 5 minutes or so

DVD goes in > MakeMKV checks IMDb and gets a proper DVD name > MakeMKV Rips
DVD does not get ejected, maybe it will get added to later versions

Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.2, 2013-01-23 18:40:18 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT

Enough with these comments, on to the code
"""

#
#   IMPORTS
#

import os
import ConfigParser
from makemkv import makeMKV
from timer import Timer

#
#   CONFIG VARIABLES
#

REAL_PATH = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.RawConfigParser()
config.read('%s/../settings.cfg' % REAL_PATH)

MKV_SAVE_PATH = config.get('MAKEMKV', 'save_path')
MKV_MIN_LENGTH = config.getint('MAKEMKV', 'min_length')
MKV_CACHE_SIZE = config.getint('MAKEMKV', 'cache_MB')
MKV_TEMP_OUTPUT = config.get('MAKEMKV', 'temp_output')
USE_HANDBRAKE = config.getboolean('MAKEMKV', 'handbrake')

#
#   CODE
#

MKVapi = makeMKV()

if (MKVapi.findDisc(MKV_TEMP_OUTPUT)):
    movieTitle = MKVapi.getTitle()

    if not os.path.exists('%s/%s' % (MKV_SAVE_PATH, movieTitle)):
        os.makedirs('%s/%s' % (MKV_SAVE_PATH, movieTitle))

        stopwatch = Timer()

        if MKVapi.ripDisc(path=MKV_SAVE_PATH,
                length=MKV_MIN_LENGTH,
                cache=MKV_CACHE_SIZE,
                queue=USE_HANDBRAKE,
                output=MKV_TEMP_OUTPUT):

            stopwatch.stop()

            print ("It took %s minutes to complete the ripping of %s"
                %
                (stopwatch.getTime(), movieTitle))

        else:
            stopwatch.stop()
            print "MakeMKV did not did not complete successfully"

    else:
        print "Movie folder already exists, will not overwrite."

else:
    print "Could not find valid DVD in drive list"
