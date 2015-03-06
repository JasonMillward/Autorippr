"""
FileBot class


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.6.2, 2014-12-03 20:12:25 ACDT $;
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
        """
            Renames movie file upon successful database lookup

            Inputs:
                dbMovie (Obj): Movie database object

            Outputs:
                Bool    Was lookup successful
        """
        proc = subprocess.Popen(
            [
                'filebot',
                '-rename',
                "%s/%s" % (dbMovie.path, dbMovie.filename),
                '--q',
                "\"%s\"" % dbMovie.moviename,
                '-non-strict',
                '--db',
                'OpenSubtitles'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        (results, errors) = proc.communicate()

        if proc.returncode is not 0:
            self.log.error(
                "Filebot (rename) returned status code: %d" % proc.returncode)

        renamedMovie = ""
        checks = 0

        if len(results) is not 0:
            lines = results.split("\n")
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
        """
            Downloads subtitles of specified language

            Inputs:
                dbMovie (Obj): Movie database object
                lang    (Str): Language of subtitles to download

            Outputs:
                Bool    Was download successful
        """
        proc = subprocess.Popen(
            [
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
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        (results, errors) = proc.communicate()

        if proc.returncode is not 0:
            self.log.error(
                "Filebot (get_subtitles) returned status code: %d" % proc.returncode)

        checks = 0

        if len(results) is not 0:
            lines = results.split("\n")
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
