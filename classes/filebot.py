"""
FileBot class


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import os
import subprocess
import logger


class filebot(object):

    def __init__(self, debug):
        self.log = logger.logger("Filebot", debug)

    def rename(self):
        #   filebot -rename title00.mkv --q [Movie Name] -non-strict
        #   [MOVE] Rename [/tmp/Euro Trip G1/Road Trip (2000).mkv] to [EuroTrip (2004).mkv]
        pass

    def subtitles(self):
        #   filebot -get-missing-subtitles --lang
        # Matched
        # Fetching
        # Writing
        pass
