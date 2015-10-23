"""
Simple logging class


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.7-test2, 2015-05-11 07:48:38 ACST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import logging
import os
import sys


class Logger(object):

    def __init__(self, name, debug, silent):
        self.silent = silent

        frmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            "%Y-%m-%d %H:%M:%S"
        )

        if debug:
            loglevel = logging.DEBUG
        else:
            loglevel = logging.INFO

        self.createhandlers( frmt, name, loglevel )

    def createhandlers(self, frmt, name, loglevel):
        self.log = logging.getLogger(name)
        self.log.setLevel(loglevel)

        if not self.silent:
            self.sh = logging.StreamHandler(sys.stdout)
            self.sh.setLevel(loglevel)
            self.sh.setFormatter(frmt)
            self.log.addHandler(self.sh)

        DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.fh = logging.FileHandler('%s/autorippr.log') % DIR
        self.fh.setLevel(loglevel)
        self.fh.setFormatter(frmt)
        self.log.addHandler(self.fh)


    def __del__(self):
        if not self.silent:
            self.log.removeHandler(self.sh)
        self.log.removeHandler(self.fh)
        self.log = None

    def debug(self, msg):
        self.log.debug(msg)

    def info(self, msg):
        self.log.info(msg)

    def warn(self, msg):
        self.log.warn(msg)

    def error(self, msg):
        self.log.error(msg)

    def critical(self, msg):
        self.log.critical(msg)
