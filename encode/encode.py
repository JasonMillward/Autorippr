"""
HandBrake queue parser

Uses MakeMKV to watch for movies inserted into DVD/BD Drives
Looks up movie title on IMDb for saving into seperate directory

Automaticly checks for existing directory/movie and will NOT overwrite existing
files or folders
Checks minimum length of video to ensure movie is ripped not previews or other
junk that happens to be on the DVD

Required for use
* Python
* MakeMKV
* IMDbPy

This script can be run with a simple cron, every 5 minutes or so.
DVD goes in > MakeMKV checks IMDb and gets a proper DVD name > MakeMKV Rips
DVD does not get ejected, maybe it will get added to later versions

Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.1, 2013-01-15 17:52:00 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT

Enough with these comments, on to the code
"""

#
#   IMPORTS
#

import os
import ConfigParser
from handbrake import handbrake

#
#   CONFIG VARIABLES
#

REAL_PATH = os.path.dirname(os.path.realpath(__file__))

config = ConfigParser.RawConfigParser()
config.read('%s/../settings.cfg' % REAL_PATH)

HB_NICE = config.getint('HANDBRAKE', 'nice')
HB_CLI = config.get('HANDBRAKE', 'com')
HB_OUT = config.get('HANDBRAKE', 'temp_output')

#
#   CODE
#

hb = handbrake()

if hb.findProcess() == False:
    if hb.loadMovie():
        hb.convert(args=HB_CLI, nice=HB_NICE, output=HB_OUT)
    else:
        print "Queue does not exist or is empty"
else:
    print "Process already running skipper"
