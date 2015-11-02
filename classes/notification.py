"""
Notification Class


Released under the MIT license
Copyright (c) 2014, Jacob Carrigan

@category   misc
@version    $Id: 1.7-test2, 2015-05-11 07:48:38 ACST $;
@author     Jacob Carrigan
@license    http://opensource.org/licenses/MIT
"""

import os
import logger

class Notification(object):

    def __init__(self, config):
        self.config = config['notification']

    def _send(self, status):
        for method in self.config:
            if self.config[ method ]['enable']:
                print method

    def rip_complete(self,dbvideo):

        status = 'Rip of %s complete' % dbvideo.vidname
        self._send(status)

    def compress_complete(self,dbvideo):

        status = 'Compress of %s complete' % dbvideo.vidname
        self._send(status)

    def extra_complete(self,tracks,dbvideo):

        status = 'Extra of %s complete' % dbvideo.vidname
        self._send(status)
