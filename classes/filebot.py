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
            "\"%s\"" % dbMovie.moviename,
            '-non-strict',
            '--db',
            'OpenSubtitles'
        ]

        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        output = proc.stdout.read()
        renamedMovie = ""
        checks = 0

        if len(output) is not 0:
            lines = output.split("\n")
            for line in lines:
                self.log.debug(line.strip())
                if "MOVE" in line:
                    renamedMovie = line.split("] to [", 1)[1].rstrip(']')
                    checks += 1

                if "Processed" in line:
                    checks += 1

                if "Done" in line:
                    checks += 1

        if checks >= 3 and renamedMovie:
            return [True, renamedMovie]
        else:
            return [False]

    def get_subtitles(self, dbMovie, lang):
        command = [
            'filebot',
            '-get-subtitles',
            dbMovie.path,
            '--q',
            "\"%s\"" % dbMovie.moviename,
            '--lang',
            lang,
            '--output',
            'srt',
            '--encoding',
            'utf8',
            '-non-strict'
        ]

        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        checks = 0

        if len(output) is not 0:
            lines = output.split("\n")
            for line in lines:
                self.log.debug(line.strip())

                if "Processed" in line:
                    checks += 1

                if "Done" in line:
                    checks += 1

        if checks >= 2:
            return True
        else:
            return False
