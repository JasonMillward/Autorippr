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

    def rename(self, dbMovie):

        command = [
            'filebot',
            '-rename',
            "%s/%s" % (dbMovie.path, dbMovie.filename),
            '--q',
            dbMovie.moviename,
            '-non-strict'
        ]

        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        print  proc.stdout.read()

        #   filebot -rename title00.mkv --q [Movie Name]
        #   [MOVE] Rename [/tmp/Euro Trip G1/Road Trip (2000).mkv] to [EuroTrip (2004).mkv]


    def subtitles(self):
        #   filebot -get-missing-subtitles --lang
        # Matched
        # Fetching
        # Writing
        pass
