"""
HandBrake CLI Wrapper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.7-test4, 2015-11-09 12:30:44 ACDT $;
@author     Jason Millward
@license    http://opensource.org/licenses/MIT
"""

import os
import re
import subprocess
import logger
import database


class HandBrake(object):

    def __init__(self, debug, compressionpath, vformat, silent):
        self.log = logger.Logger("HandBrake", debug, silent)
        self.compressionPath = compressionpath
        self.vformat = vformat

    def compress(self, nice, args, dbvideo):
        """
            Passes the necessary parameters to HandBrake to start an encoding
            Assigns a nice value to allow give normal system tasks priority

            Inputs:
                nice    (Int): Priority to assign to task (nice value)
                args    (Str): All of the handbrake arguments taken from the
                                settings file
                output  (Str): File to log to. Used to see if the job completed
                                successfully

            Outputs:
                Bool    Was convertion successful
        """
        checks = 0

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
        command = 'nice -n {0} {1}HandBrakeCLI --verbose -i "{2}" -o "{3}" {4}'.format(
            nice,
            self.compressionPath,
            invid,
            outvid,
            ' '.join(args)
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
                "HandBrakeCLI (compress) returned status code: %d" % proc.returncode)

        if results is not None and len(results) is not 0:
            lines = results.split("\n")
            for line in lines:
                if "Encoding: task" not in line:
                    self.log.debug(line.strip())

                if "average encoding speed for job" in line:
                    checks += 1

                if "Encode done!" in line:
                    checks += 1

                if "ERROR" in line and "opening" not in line:
                    self.log.error(
                        "HandBrakeCLI encountered the following error: ")
                    self.log.error(line)

                    return False

        if checks >= 2:
            self.log.debug("HandBrakeCLI Completed successfully")

            database.update_video(
                dbvideo, 6, filename="%s" % (
                    vidname
                ))

            return True
        else:
            return False
