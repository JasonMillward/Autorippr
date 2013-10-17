"""
MakeMKV CLI Wrapper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.4, 2013-04-03 09:41:53 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import subprocess
import imdb
import os
import re
from database import dbCon


class makeMKV(object):
    """
        This class acts as a python wrapper to the MakeMKV CLI.
    """

    def __init__(self):
        """
            Initialises the variables that will be used in this class

            Inputs:
                None

            Outputs:
                None
        """
        self.discIndex = 0
        self.movieName = ""
        self.path = ""
        self.movieName = ""
        self.imdbScaper = imdb.IMDb()

    def _queueMovie(self):
        """
            Adds the recently ripped movie to the queue db for the compression
                script to handle later on

            Inputs:
                None

            Outputs:
                None
        """
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


    def _cleanTitle(self):
        """
            Removes the extra bits in the title and removes whitespace

            Inputs:
                None

            Outputs:
                None
        """
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


    def ripDisc(self, path, length, cache, queue, output):
        """
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
        self.path = path

        fullPath = '%s/%s' % (self.path, self.movieName)
        command = [
            'makemkvcon',
            'mkv',
            'disc:%s' % self.discIndex,
            '0',
            fullPath,
            '--cache=%d' % cache,
            '--noscan',
            '--minlength=%d' % length
        ]

        proc = subprocess.Popen(
            command,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE
        )

        if proc.stderr is not None:
            output = proc.stderr.read()
            if len(output) is not 0:
                print "MakeMKV encountered the following error: "
                print output
                print ""
                return False

        checks = 0
        output = proc.stdout.read()
        lines = output.split("\n")
        for line in lines:
            if "skipped" in line:
                continue

            badStrings = [
                "failed",
                "Fail",
                "error"
            ]

            if any(x in line.lower() for x in badStrings):
                print line
                return False

            if "Copy complete" in line:
                checks += 1

            if "titles saved" in line:
                checks += 1

        if checks >= 2:
            if queue:
                self._queueMovie()
            return True
        else:
            return False

    def findDisc(self, output):
        """
            Use makemkvcon to list all DVDs or BDs inserted
            If more then one disc is inserted, use the first result

            Inputs:
                output  (Str): Temp file to save output to

            Outputs:
                Success (Bool)
        """
        proc = subprocess.Popen(
            ['makemkvcon', '-r', 'info'],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        output = proc.stderr.read()
        if proc.stderr is not None:
            if len(output) is not 0:
                print "MakeMKV encountered the following error: "
                print output
                print ""
                return False

        output = proc.stdout.read()
        if "This application version is too old." in output:
            print "Your MakeMKV version is too old." \
                "Please download the latest version at http://www.makemkv.com" \
                " or enter a registration key to continue using MakeMKV."

            return False

        # Passed the simple tests, now check for disk drives
        lines = output.split("\n")
        for line in lines:
            if line[:4] == "DRV:":
                if "/dev/" in line:
                    drive = line.split(',')
                    self.discIndex = drive[0].replace("DRV:", "")
                    self.movieName = drive[5]
                    break

        # Python :(
        if len(str(self.discIndex)) is 0 or len(str(self.movieName)) < 4:
            return False
        else:
            return True

    def getTitle(self):
        """
            Returns the current movies title

            Inputs:
                None

            Outputs:
                movieName   (Str)
        """
        self._cleanTitle()

        result = self.imdbScaper.search_movie(self.movieName, results=1)

        if len(result) > 0:
            self.movieName = result[0]

        return self.movieName
