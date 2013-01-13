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

MKV_SAVE_PATH = config.getint('HANDBRAKE', 'nice')
MKV_SAVE_PATH = config.get('HANDBRAKE', 'com')

hb = handbrake()

if hb.findProcess() == False:
    if hb.loadMovie():
        print "Found movie string"
    else:
        print "queue does not exist"
