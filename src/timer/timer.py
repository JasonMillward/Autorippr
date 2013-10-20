"""
Simple timer class

This class provides simple functions for timing operations


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

#
#   IMPORTS
#

import datetime

#
#   CODE
#


class Timer(object):

    def __init__(self):
        self.startTime = datetime.datetime.now()

    def stop(self):
        endTime = datetime.datetime.now()
        totalTime = endTime - self.startTime
        self.minutes = totalTime.seconds / 60

    def getTime(self):
        return self.minutes
