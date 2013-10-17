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
@version    $Id: 1.4, 2013-04-03 09:41:53 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT

Enough with these comments, on to the code
"""

import os
import sys
import ConfigParser
from makemkv import makeMKV
from timer import Timer

DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = "%s/../settings.cfg" % DIR

def readValue(key):
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)
    toReturn = config.get('MAKEMKV', key)
    config = None
    return toReturn

def rip():
    MKV_SAVE_PATH = readValue('save_path')
    MKV_MIN_LENGTH = readValue('min_length')
    MKV_CACHE_SIZE = readValue('cache_MB')
    MKV_TEMP_OUTPUT = readValue('temp_output')
    USE_HANDBRAKE = readValue('handbrake')

    MKVAPI = makeMKV()

    if (MKVAPI.findDisc(MKV_TEMP_OUTPUT)):
        movieTitle = MKVAPI.getTitle()

        print movieTitle
        sys.exit()

        if not os.path.exists('%s/%s' % (MKV_SAVE_PATH, movieTitle)):
            os.makedirs('%s/%s' % (MKV_SAVE_PATH, movieTitle))

            stopwatch = Timer()

            if MKVAPI.ripDisc(path=MKV_SAVE_PATH,
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

if __name__ == '__main__':
    rip()
