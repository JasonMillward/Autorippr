"""
FFmpeg Wrapper


Released under the MIT license
Copyright (c) 2014, Ian Bird

@category   misc
@author     Ian Bird
@license    http://opensource.org/licenses/MIT
"""

import os
import subprocess
import logger

from compression import compression

class ffmpeg(compression):

    def __init__(self, debug):
        self.log = logger.logger("FFmpeg", debug)

    def compress(self, nice, args, dbMovie):
        """
            Passes the nessesary parameters to FFmpeg to start an encoding
            Assigns a nice value to allow give normal system tasks priority

            Upon successful encode, clean up the output logs and remove the
                input movie as they are no longer needed

            Inputs:
                nice    (Int): Priority to assign to task (nice value)
                args    (Str): All of the FFmpeg arguments taken from the
                                settings file
                output  (Str): File to log to. Used to see if the job completed
                                successfully

            Outputs:
                Bool    Was convertion successful
        """

        moviename = "%s.mkv" % dbMovie.moviename
        inMovie = "%s/%s" % (dbMovie.path, dbMovie.filename)
        outMovie = "%s/%s" % (dbMovie.path, moviename)

        command = 'nice -n {0} ffmpeg -i "{1}" {2} "{3}"'.format(
            nice,
            inMovie,
            ' '.join(args),
            outMovie
        )

        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True
        )
        (results, errors) = proc.communicate()

        if proc.returncode is not 0:
            self.log.error("FFmpeg (compress) returned status code: %d" % proc.returncode)
            return False

        return True
