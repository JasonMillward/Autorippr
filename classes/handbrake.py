"""
HandBrake CLI Wrapper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.6, 2014-07-21 18:48:00 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import os
import subprocess
import logger


class handBrake(object):

    def __init__(self, debug):
        self.log = logger.logger("HandBrake", debug)

    def _cleanUp(self, cFile):
        """
            Deletes files once HandBrake is finished with them

            Inputs:
                cFile    (Str): File path of the movie to remove

            Outputs:
                None
        """
        try:
            os.remove(cFile)
        except:
            self.log.error("Could not remove %s" % cFile)

    def check_exists(self, dbMovie):
        """
            Checks to see if the file still exists at the path set in the
                database

            Inputs:
                dbMovie (Obj): Movie database object

            Outputs:
                Bool    Does file exist

        """
        inMovie = "%s/%s" % (dbMovie.path, dbMovie.filename)

        if os.path.isfile(inMovie):
            return True

        else:
            self.log.debug(inMovie)
            self.log.error("Input file no longer exists")
            return False

    def convert(self, nice, args, dbMovie):
        """
            Passes the nessesary parameters to HandBrake to start an encoding
            Assigns a nice value to allow give normal system tasks priority

            Upon successful encode, clean up the output logs and remove the
                input movie as they are no longer needed

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

        moviename = "%s.mkv" % dbMovie.moviename
        inMovie = "%s/%s" % (dbMovie.path, dbMovie.filename)
        outMovie = "%s/%s" % (dbMovie.path, moviename)

        proc = subprocess.Popen(
            [
                'nice',
                '-n',
                str(nice),
                'HandBrakeCLI',
                '--verbose',
                str(1),
                '-i',
                str(inMovie),
                '-o',
                str(outMovie),
                args
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        # I'm a little confused here
        # handbrake cli spits out good information into stderr
        # so I'll parse stderr as stdout

        if proc.stderr is not None:
            output = proc.stderr.read()
            if len(output) is not 0:
                lines = output.split("\n")
                for line in lines:
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
            self._cleanUp(cFile=inMovie)

            return True
        else:
            return False
