"""
HandBrake CLI Wrapper + Queue Handler


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


class handBrake(object):

    def __init__(self, debug):
        self.log = logger.logger("Handbrake CLI", debug)

    def _cleanUp(self, cFile):
        """ Function:   _cleanUp
                Removes the log file and the input movie because these files are
                    no longer needed by this script

            Inputs:
                log         (Str): File path of the log to remove
                oldMovie    (Str): File path of the movie to remove

            Outputs:
                None
        """
        try:
            os.remove(cFile)
        except:
            self.log.error("Could not remove %s" % cFile)

    def check_exists(self, moviedb):
        inMovie = "%s/%s" % (moviedb.path, moviedb.filename)

        if not os.path.isfile(inMovie):
            self.log.debug(inMovie)
            self.log.error("Input file no longer exists")
            return False

    def convert(self, nice, args, moviedb):
        """ Function:   convert
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
                None
        """
        checks = 0

        moviename = "%s.mkv" % moviedb.moviename
        inMovie = "%s/%s" % (moviedb.path, moviedb.filename)
        outMovie = "%s/%s" % (moviedb.path, moviename)

        command = [
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
            args,
            '2>&1'
        ]

        # Subtitle changes
        # -F, --subtitle-forced   Only display subtitles from the selected stream if
        #  <string>          the subtitle has the forced flag set.
        # -N, --native-language   Specifiy your language preference. When the first
        # -F --subtitle scan -N eng

        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # I'm a little confused here
        # handbrake cli spits out stdout into stderr
        # so I'll parse both stderr and stdout

        if proc.stderr is not None:
            output = proc.stderr.read()
            if len(output) is not 0:
                lines = output.split("\n")
                for line in lines:
                    #self.log.debug(line.strip())

                    if "average encoding speed for job" in line:
                        checks += 1

                    if "Encode done!" in line:
                        checks += 1

                    if "ERROR" in line and "opening" not in line:
                        self.log.error("HandBrakeCLI encountered the following error: ")
                        self.log.error(line)

                        return False

                if checks >= 2:
                    self.log.debug("HandBrakeCLI Completed successfully")
                    self._cleanUp(cFile=inMovie)

                    return True
                else:
                    return False

