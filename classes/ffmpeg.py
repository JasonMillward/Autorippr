"""
FFmpeg Wrapper


Released under the MIT license
Copyright (c) 2014, Ian Bird

@category   misc
@version    $Id: 1.7-test4, 2015-11-09 12:30:44 ACDT $;
@author     Ian Bird
@license    http://opensource.org/licenses/MIT
"""

import os
import subprocess
from . import logger


class FFmpeg(object):

    def __init__(self, debug, silent, vformat):
        self.log = logger.Logger("FFmpeg", debug, silent)
        self.vformat = vformat

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

        if (dbvideo.vidtype == "tv"):
            # Query the SQLite database for similar titles (TV Shows)
            vidname = re.sub(r'D(\d)', '', dbvideo.vidname)
            vidqty = database.search_video_name(vidname)
            if vidqty == 0:
                vidname = "%sE1.%s" % (vidname, self.vformat)
            else:
                vidname = "%sE%s.%s" % (vidname, str(vidqty + 1), self.vformat)
        else:
            vidname = "%s.%s" % (dbvideo.vidname, self.vformat)

        invid = "%s/%s" % (dbvideo.path, dbvideo.filename)
        outvid = "%s/%s" % (dbvideo.path, vidname)

        command = 'nice -n {0} ffmpeg -i "{1}" {2} "{3}"'.format(
            nice,
            invid,
            ' '.join(args),
            outvid
        )

        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True
        )
        (results, errors) = proc.communicate()

        if proc.returncode is not 0:
            self.log.error(
                "FFmpeg (compress) returned status code: %d" % proc.returncode)
            return False

        return True
