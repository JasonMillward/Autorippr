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

#
#   CODE
#


class Logger(object):

    def __init__(self, name, debug):
        self.log = logging.getLogger('rip')
        self.log.setLevel(logging.DEBUG)

        logfile = logging.FileHandler('makeMKV-Autoripper.log')
        logfile.setLevel(logging.DEBUG)

        frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logfile.setFormatter(frmt)
        
        self.log.addHandler(logfile)

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
