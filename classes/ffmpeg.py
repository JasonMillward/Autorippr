"""
FFmpeg Wrapper


Released under the MIT license
Copyright (c) 2014, Ian Bird

@category   misc
@version    $Id: 1.7-testing, 2015-03-09 21:25:58 ACDT $;
@author     Ian Bird
@license    http://opensource.org/licenses/MIT
"""

import os
import subprocess
import logger

class FFmpeg(object):

    def __init__(self, debug, silent):
        self.log = logger.Logger("FFmpeg", debug, silent)

    def compress(self, nice, args, dbmovie):
        """
            Passes the necessary parameters to FFmpeg to start an encoding
            Assigns a nice value to allow give normal system tasks priority


            Inputs:
                nice    (Int): Priority to assign to task (nice value)
                args    (Str): All of the FFmpeg arguments taken from the
                                settings file
                output  (Str): File to log to. Used to see if the job completed
                                successfully

            Outputs:
                Bool    Was convertion successful
        """

        moviename = "%s.mkv" % dbmovie.moviename
        inmovie = "%s/%s" % (dbmovie.path, dbmovie.filename)
        outmovie = "%s/%s" % (dbmovie.path, moviename)

        command = 'nice -n {0} ffmpeg -i "{1}" {2} "{3}"'.format(
            nice,
            inmovie,
            ' '.join(args),
            outmovie
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
