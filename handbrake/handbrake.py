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

#
#   IMPORTS
#

import os
import commands
from database import dbCon
from logger import Logger

#
#   CODE
#


class HandBrake(object):

    def __init__(self, debugLevel):
        self.db = dbCon()
        self.log = Logger("handbrake", True)

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

        commands.getstatusoutput(
            'nice -n %d HandBrakeCLI --verbose 1 -i "%s" -o "%s" %s 2> %s'
            %
            (nice, inMovie, outMovie, args, output))

        checks = 0
        try:
            tempFile = open(output, 'r')
            for line in tempFile.readlines():
                if "average encoding speed for job" in line:
                    checks += 1
                if "Encode done!" in line:
                    checks += 1
        except:
            self.log.info("Could not read output file, no cleanup will be done")

        if checks == 2:
            self._updateQueue(uStatus="Complete", uAdditional="Job Done")
            self._cleanUp(cFile=inMovie)
            self._cleanUp(cFile=output)
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
