"""
MakeMKV CLI Wrapper

This class acts as a python wrapper to the MakeMKV CLI.


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.4, 2013-04-03 09:41:53 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

#
#   IMPORTS
#

import commands
import imdb
import os
import re
from database import dbCon

#
#   CODE
#


class makeMKV(object):

    """ Function:   __init__
            Initialises the variables that will be used in this class

        Inputs:
            None

        Outputs:
            None
    """
    def __init__(self):
        self.discIndex = 0
        self.movieName = ""
        self.path = ""
        self.movieName = ""
        self.imdbScaper = imdb.IMDb()

    """ Function:   _queueMovie
            Adds the recently ripped movie to the queue db for the compression
                script to handle later on

        Inputs:
            None

        Outputs:
            None
    """
    def _queueMovie(self):
        db = dbCon()
        movie = ""

        os.chdir('%s/%s' % (self.path, self.movieName))
        for files in os.listdir("."):
            if files.endswith(".mkv"):
                movie = files
                break

        path = "%s/%s" % (self.path, self.movieName)
        outMovie = "%s.mkv" % self.movieName
        db.insert(path, inMovie=movie, outMovie=outMovie)

    """ Function:   _cleanTitle
            Removes the extra bits in the title and removes whitespace

        Inputs:
            None

        Outputs:
            None
    """
    def _cleanTitle(self):
        tmpName = self.movieName
        # A little fix for extended editions (eg; Die Hard 4)
        tmpName = tmpName.title().replace("Extended_Edition", "")

        # Remove Special Edition
        tmpName = tmpName.replace("Special_Edition", "")

        # Remove Disc X from the title
        tmpName = re.sub(r"Disc_(\d)", "", tmpName)

        # Clean up the disc title so IMDb can identify it easier
        tmpName = tmpName.replace("\"", "").replace("_", " ")

        # Clean up the edges and remove whitespace
        self.movieName = tmpName.strip()

    """ Function:   ripDisc
            Passes in all of the arguments to makemkvcon to start the ripping
                of the currently inserted DVD or BD

        Inputs:
            path    (Str):  Where the movie will be saved to
            length  (Int):  Minimum length of the main movie
            cache   (Int):  Cache in MB
            queue   (Bool): Save movie into queue for compressing later
            output  (Str):  Temp file to save output to

        Outputs:
            Success (Bool)
    """
    def ripDisc(self, path, length, cache, queue, output):
        self.path = path

        args = (" --cache=%d --noscan --minlength=%d > %s"
            % (cache, length, output))

        commands.getstatusoutput(
            'makemkvcon mkv disc:%s 0 "%s/%s" %s'
            %
            (self.discIndex, self.path, self.movieName, args))

        checks = 0
        try:
            tempFile = open(output, 'r')
            for line in tempFile.readlines():
                if "Copy complete" in line:
                    checks += 1
                if "titles saved" in line:
                    checks += 1
        except:
            print "Could not read output file"

        if checks >= 2:
            if queue:
                self._queueMovie()
            return True
        else:
            return False

    """ Function:   findDisc
            Use makemkvcon to list all DVDs or BDs inserted
            If more then one disc is inserted, use the first result

        Inputs:
            output  (Str): Temp file to save output to

        Outputs:
            Success (Bool)
    """
    def findDisc(self, output):
        commands.getstatusoutput('makemkvcon -r info > %s' % output)

        # Open the info file from /tmp/
        tempFile = open(output, 'r')
        for line in tempFile.readlines():
            if line[:4] == "DRV:":
                if "/dev/" in line:
                    drive = line.split(',')
                    self.discIndex = drive[0].replace("DRV:", "")
                    self.movieName = drive[5]
                    break

        if len(str(self.discIndex)) is 0 or len(str(self.movieName)) < 4:
            return False
        else:
            return True

    """ Function:   getTitle
            Returns the current movies title

        Inputs:
            None

        Outputs:
            movieName   (Str)
    """
    def getTitle(self):
        self._cleanTitle()

        result = self.imdbScaper.search_movie(self.movieName, results=1)

        if len(result) > 0:
            self.movieName = result[0]

        return self.movieName
