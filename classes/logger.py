"""
Simple logging class


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.6.1, 2014-08-18 10:42:00 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import logging
import sys


class logger(object):

    def __init__(self, name, debug):
        frmt = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            "%Y-%m-%d %H:%M:%S"
        )

        if debug:
            logLevel = logging.DEBUG
        else:
            logLevel = logging.INFO

        self.sh = logging.StreamHandler(sys.stdout)
        self.sh.setLevel(logLevel)
        self.sh.setFormatter(frmt)

        self.fh = logging.FileHandler('autorippr.log')
        self.fh.setLevel(logLevel)
        self.fh.setFormatter(frmt)

        self.log = logging.getLogger(name)
        self.log.setLevel(logLevel)
        self.log.addHandler(self.sh)
        self.log.addHandler(self.fh)

    def __del__(self):
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
