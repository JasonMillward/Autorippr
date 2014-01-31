"""
Simple logging class

This class provides a cleaner way for adding logging to every file


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

import logging
import sys

#
#   CODE
#


class Logger(object):

    def __init__(self, name, debug):
        frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logLevel = logging.INFO

        if debug == True:
            logLevel = logging.DEBUG

        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logLevel)
        sh.setFormatter(frmt)

        fh = logging.FileHandler('makeMKV-Autoripper.log')
        fh.setLevel(logLevel)
        fh.setFormatter(frmt)

        self.log = logging.getLogger(name)
        self.log.setLevel(logging.INFO)
        self.log.addHandler(sh)
        self.log.addHandler(fh)

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
