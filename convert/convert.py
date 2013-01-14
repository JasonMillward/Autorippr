#!/usr/bin/env python

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

hb = handbrake()

if hb.findProcess() == False:
    if hb.loadMovie():
        hb.convert(args=HB_CLI, nice=HB_NICE, out=HB_OUT)
    else:
        print "Queue does not exist"
else:
    print "Process already running skipper"
