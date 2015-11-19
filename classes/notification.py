"""
Notification Class


Released under the MIT license
Copyright (c) 2014, Jason Millward

@category   misc
@version    $Id: 1.7-test4, 2015-11-09 12:30:44 ACDT $;
@author     Jason Millward
@license    http://opensource.org/licenses/MIT
"""

import os
import importlib
import pprint
from . import logger

class Notification(object):

    def __init__(self, config, debug, silent):
        self.config = config['notification']
        self.debug = debug
        self.silent = silent
        self.log = logger.Logger("Notification", debug, silent)

    def import_from(self, module, name, config):
        module = __import__(module, fromlist=[name])
        class_ = getattr(module, name)
        return class_(config, self.debug, self.silent)

    def _send(self, status):
        for method in self.config['methods']:
            if bool(self.config['methods'][method]['enable']):
                try:
                    method_class = self.import_from('classes.{}'.format(
                        method), method.capitalize(), self.config['methods'][method])
                    method_class.send_notification(status)
                    del method_class
                except ImportError:
                    self.log.error(
                        "Error loading notification class: {}".format(method))

    def rip_complete(self, dbvideo):

        status = 'Rip of %s complete' % dbvideo.vidname
        self._send(status)

    def rip_fail(self, dbvideo):

        status = 'Rip of %s failed' % dbvideo.vidname
        self._send(status)

    def compress_complete(self, dbvideo):

        status = 'Compress of %s complete' % dbvideo.vidname
        self._send(status)

    def compress_fail(self, dbvideo):

        status = 'Compress of %s failed' % dbvideo.vidname
        self._send(status)

    def extra_complete(self, dbvideo):

        status = 'Extra of %s complete' % dbvideo.vidname
        self._send(status)
