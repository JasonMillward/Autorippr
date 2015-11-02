"""
Notification Class


Released under the MIT license
Copyright (c) 2014, Jason Millward

@category   misc
@version    $Id: 1.7-test2, 2015-05-11 07:48:38 ACST $;
@author     Jason Millward
@license    http://opensource.org/licenses/MIT
"""

import os
import logger
import importlib
import pprint

class Notification(object):

    def __init__(self, config):
        self.config = config['notification']
        self._send("test")

    def import_from(self, module, name, config):
        module = __import__(module, fromlist=[name])
        class_ = getattr(module, name)
        return class_(config)

    def _send(self, status):
        for method in self.config['methods']:
            if bool(self.config['methods'][ method ]['enable']):
                try:
                    method_class = self.import_from('classes.{}'.format(method), method.capitalize(), self.config['methods'][ method ])
                    method_class.send_notification(status)
                    del method_class
                except ImportError:
                    print "broke"

    def rip_complete(self,dbvideo):

        status = 'Rip of %s complete' % dbvideo.vidname
        self._send(status)

    def compress_complete(self,dbvideo):

        status = 'Compress of %s complete' % dbvideo.vidname
        self._send(status)

    def extra_complete(self,tracks,dbvideo):

        status = 'Extra of %s complete' % dbvideo.vidname
        self._send(status)
