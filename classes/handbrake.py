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
import database
import logger


class handBrake(object):

    def __init__(self, debug):
        self.log = logger.logger("Handbrake", debug)

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
    def _updateQueue(self, uStatus):
        database.update_movie(self.dbMovie, uStatus)

    """ Function:   loadMovie
            Check to see if the queue file exists, if it does load the first
                line and proccess it for the rest of the script to use

        Inputs:
            None

        Outputs:
            None
    """
    def loadMovie(self):
        movie = database.next_movie()

        if movie is not None:
            self.ID = movie.movieid
            self.path = movie.path
            self.inputMovie = movie.filename
            self.outputMovie = "%s.mkv" % movie.moviename
            self.dbMovie = movie

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
    def convert(self, nice, args):
        checks = 0
        inMovie = "%s/%s" % (self.path, self.inputMovie)
        outMovie = "%s/%s" % (self.path, self.outputMovie)

        if not os.path.isfile(inMovie):
            self.log.debug(inMovie)
            self.log.error("Input file no longer exists")
            return False

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
            args
        ]

        # Subtitle changes
        # -F, --subtitle-forced   Only display subtitles from the selected stream if
        #  <string>          the subtitle has the forced flag set.
        # -N, --native-language   Specifiy your language preference. When the first
        # -F --subtitle scan -N eng

        proc = subprocess.Popen(
            command,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        if proc.stderr is not None:
            output = proc.stderr.read()
            if len(output) is not 0:
                self.log.error("HandBakeCLI encountered the following error: ")
                lines = output.split("\n")
                for line in lines:
                    self.log.error(line.strip())
                    database.insert_history(self.dbMovie, line, 4)
                self._updateQueue(2)
                return False

        output = proc.stdout.read()
        lines = output.split("\n")
        for line in lines:
            self.log.debug(line.strip())
            if "average encoding speed for job" in line:
                checks += 1
            if "Encode done!" in line:
                checks += 1
            if "ERROR" in line:
                self.log.error("HandBakeCLI encountered the following error: ")
                self.log.error(line)
                self._updateQueue(2)
                database.insert_history(self.dbMovie, line, 4)
                return False

        if checks == 2:
            self.log.debug("HandBakeCLI Completed successfully")
            self._updateQueue(6)
            self._cleanUp(cFile=inMovie)
            self._cleanUp(cFile=output)
            database.insert_history(
                self.dbMovie,
                "HandBakeCLI Completed successfully"
            )
            return True
        else:
            self._updateQueue(2)
            database.insert_history(self.dbMovie, "Handbrake failed", 4)
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
