"""
Simple timer class


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import datetime


class stopwatch(object):

    def __enter__(self):
        self.startTime = datetime.datetime.now()
        return self

    def __exit__(self, *args):
        endTime = datetime.datetime.now()
        totalTime = endTime - self.startTime
        self.minutes = totalTime.seconds / 60

