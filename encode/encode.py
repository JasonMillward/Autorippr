"""
HandBrake queue parser

Uses HandBrake to encode movies ripped by makeMKV


This script can be run with a simple cron, every hour should be fine

An optional script used to rename and compress movies to an acceptable standard
which still delivers quallity audio and video but reduces the file size
dramatly.
Using a nice value of 20 by default, it runs HandBrake as a background task
that allows other critical tasks to complete first.

Using this script with the auto ripper allows for multiple movies to be ripped
and encoded with very little effot.


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.1, 2013-01-19 19:45:00 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
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
