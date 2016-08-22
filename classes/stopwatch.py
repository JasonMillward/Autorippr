# -*- coding: utf-8 -*-
"""
Simple StopWatch


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.7.0, 2016-08-22 14:53:29 ACST $;
@author     Jason Millward
@license    http://opensource.org/licenses/MIT
"""

import datetime


class StopWatch(object):

    def __enter__(self):
        self.startTime = datetime.datetime.now()
        return self

    def __exit__(self, *args):
        endtime = datetime.datetime.now()
        totaltime = endtime - self.startTime
        self.minutes = totaltime.seconds / 60
