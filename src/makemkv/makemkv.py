"""
MakeMKV CLI Wrapper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import subprocess
import imdb
import os
import re
import csv
from database import dbCon


class makeMKV(object):
    """
        This class acts as a python wrapper to the MakeMKV CLI.
    """

    def __init__(self, minLength, cacheSize, useHandbrake):
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
        self.minLength = int(minLength)
        self.cacheSize = int(cacheSize)
        self.useHandbrake = bool(useHandbrake)

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


    def setTitle(self, movieName):
        self.movieName = movieName


    def setIndex(self, index):
        self.discIndex = int(index)


    def ripDisc(self, path, output):
        """
            Passes in all of the arguments to makemkvcon to start the ripping
                of the currently inserted DVD or BD

            Inputs:
                path    (Str):  Where the movie will be saved to
                output  (Str):  Temp file to save output to

            Outputs:
                Success (Bool)
        """
        self.path = path

        fullPath = '%s/%s' % (self.path, self.movieName)
        command = [
            'makemkvcon',
            'mkv',
            'disc:%d' % self.discIndex,
            '0',
            fullPath,
            '--cache=%d' % self.cacheSize,
            '--noscan',
            '--minlength=%d' % self.minLength
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
            if self.useHandbrake:
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
        drives = []
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
                return []

        output = proc.stdout.read()
        if "This application version is too old." in output:
            print "Your MakeMKV version is too old." \
                "Please download the latest version at http://www.makemkv.com" \
                " or enter a registration key to continue using MakeMKV."

            return []

        # Passed the simple tests, now check for disk drives

        lines = output.split("\n")
        for line in lines:
            if line[:4] == "DRV:":
                if "/dev/" in line:
                    out = line.split(',')

                    if len(str(out[5])) > 3:

                        drives.append(
                            {
                                "discIndex": out[0].replace("DRV:", ""),
                                "discTitle": out[5]
                            }
                        )

        return drives


    def getDiscInfo(self):
        """
            Returns information about the selected disc

            Inputs:
                None

            Outputs:
                None
        """

        proc = subprocess.Popen(
            [
                'makemkvcon',
                '-r',
                'info',
                'disc:%d' % self.discIndex,
                '--minlength=%d' % self.minLength,
                '--messages=/tmp/makemkvMessages'
            ],
            stderr=subprocess.PIPE
        )

        output = proc.stderr.read()
        if proc.stderr is not None:
            if len(output) is not 0:
                print "MakeMKV encountered the following error: "
                print output
                print ""
                return False

        print self.readMKVMessages("TCOUNT")
        print self.readMKVMessages("TINFO", 0)


    def readMKVMessages(self, search, searchIndex = None):
        """
            Returns a list of messages that match the search string

            Inputs:
                search      (Str)
                searchIndex (Str)

            Outputs:
                toReturn    (List)
        """
        toReturn = []
        with open('/tmp/makemkvMessages', 'r') as messages:
            for line in messages:
                if line[:len(search)] == search:
                    values = line.replace("%s:" % search, "").strip()

                    cr = csv.reader([values])

                    if searchIndex is not None:
                        for row in cr:
                            if int(row[0]) == int(searchIndex):
                                print row
                                toReturn.append(row[3])
                    else:
                        for row in cr:
                            toReturn.append(row[0])

        return toReturn

    def getTitle(self):
        """
            Returns the current movies title

            Inputs:
                None

            Outputs:
                movieName   (Str)
        """
        self._cleanTitle()

        # Socket or connection errors
        try:
            result = self.imdbScaper.search_movie(self.movieName, results=1)

            if len(result) > 0:
                self.movieName = result[0]

        except:
            pass

        return self.movieName
