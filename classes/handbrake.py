"""
HandBrake CLI Wrapper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.7-test2, 2015-05-11 07:48:38 ACST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import os
import subprocess
import logger

class HandBrake(object):

    def __init__(self, debug, compressionpath, vformat, silent):
        self.log = logger.Logger("HandBrake", debug, silent)
        self.compressionPath = compressionpath
        self.vformat = vformat

    def compress(self, nice, args, dbmovie):
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

        if (dbmovie.multititle):
            moviename = "%s-%s.%s" % (dbmovie.moviename, dbmovie.titleindex, self.vformat)
        else:
            moviename = "%s.%s" % (dbmovie.moviename, self.vformat)
            
        inmovie = "%s/%s" % (dbmovie.path, dbmovie.filename)
        outmovie = "%s/%s" % (dbmovie.path, moviename)
        command = 'nice -n {0} {1}HandBrakeCLI --verbose -i "{2}" -o "{3}" {4}'.format(
            nice,
            self.compressionPath,
            inmovie,
            outmovie,
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

            return True
        else:
            return False
