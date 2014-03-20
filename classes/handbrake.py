"""
HandBrake CLI Wrapper + Queue Handler

This class acts as a python wrapper to the HandBrake CLI.


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import os
import subprocess
import database
import logger


class handBrake(object):

    def __init__(self, debugLevel):
        self.db = database.database()
        self.log = logger.logger("handbrake", debugLevel)

    """ Function:   _cleanUp
            Removes the log file and the input movie because these files are
                no longer needed by this script

        Inputs:
            log         (Str): File path of the log to remove
            oldMovie    (Str): File path of the movie to remove

        Outputs:
            None
    """
    def _cleanUp(self, cFile):
        try:
            os.remove(cFile)
        except:
            self.log.error("Could not remove %s" % cFile)

    """ Function:   _updateQueue
            Removes the recently processed movie from the queue so it's not
                processed again

        Inputs:
            None

        Outputs:
            None
    """
    def _updateQueue(self, uStatus, uAdditional):
        self.db.update(uid=self.ID, status=uStatus, text=uAdditional)

    """ Function:   loadMovie
            Check to see if the queue file exists, if it does load the first
                line and proccess it for the rest of the script to use

        Inputs:
            None

        Outputs:
            None
    """
    def loadMovie(self):
        movie = self.db.getNextMovie()
        if isinstance(movie, tuple):
            self.ID = movie[0]
            self.path = movie[1]
            self.inputMovie = movie[2]
            self.outputMovie = movie[3]
            return True
        else:
            return False

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
    def convert(self, nice, args, output):
        inMovie = "%s/%s" % (self.path, self.inputMovie)
        outMovie = "%s/%s" % (self.path, self.outputMovie)

        if not os.path.isfile(inMovie):
            self.log.error("Input file no longer exists")
            return False

        command = [
            'nice',
            '-n',
            nice,
            'HandBrakeCLI',
            '--verbose',
            1,
            '-i',
            '"%s"' % inMovie,
            '-o',
            '"%s"' % outMovie,
            args,
            '2> %s' % output
        ]

        self.log.debug("HandBakeCLI commands: ")
        self.log.debug(command)

        proc = subprocess.Popen(
            command,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        )

        if proc.stderr is not None:
            output = proc.stderr.read()
            if len(output) is not 0:
                self.log.error("HandBakeCLI encountered the following error: ")
                self.log.error(output)
                return False

        output = proc.stdout.read()
        lines = output.split("\n")
        for line in lines:
            if "average encoding speed for job" in line:
                checks += 1
            if "Encode done!" in line:
                checks += 1

        if checks == 2:
            self.log.debug("HandBakeCLI Completed successfully")
            #self._updateQueue(uStatus="Complete", uAdditional="Job Done")
            #self._cleanUp(cFile=inMovie)
            #self._cleanUp(cFile=output)
            return True
        else:
            self._updateQueue(uStatus="Failed", uAdditional="HandBrake failed")
            return False

    """ Function:   getMovieTitle
            Returns the currently loaded movie title

        Inputs:
            None

        Outputs:
            self.movie  (Str): Movie title parsed from queue
    """
    def getMovieTitle(self):
        return self.outputMovie
