#!/usr/bin/env python

from handbrake import handbrake


if handbrake.findProcess() == False:
    print "Didn't find a process"
