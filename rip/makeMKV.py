"""
MakeMKV CLI Wrapper

This class acts as a python wrapper to the MakeMKV CLI.


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.1, 2013-01-15 17:52:00 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MITT
"""

#
#   IMPORTS
#

import commands
import imdb
import os
import re

#
#   CODE
#


class makeMKV(object):
    api_url = 'https://api.bitbucket.org/1.0/'

    def __init__(self):
        self.movieName = ""
        self.imdbScaper = imdb.IMDb()

    def _queueMovie(self):
        home = os.path.expanduser("~")
        if os.path.exists('%s/.makemkvautoripper' % home) == False:
            os.makedirs('%s/.makemkvautoripper' % home)

        os.chdir('%s/%s' % (self.path, self.movieName))
        for files in os.listdir("."):
            if files.endswith(".mkv"):
                movie = files
                break

        with open("%s/.makemkvautoripper/queue" % home, "a+") as myfile:
            myfile.write("%s|%s|%s|%s.mkv\n"
                %
                (self.path, self.movieName, movie, self.movieName))

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

    def ripDisc(self, path, length, cache, queue):
        self.path = path
        # Start the making of the mkv
        commands.getstatusoutput(
            'makemkvcon mkv disc:%s 0 "%s/%s" --cache=%d --noscan --minlength=%d'
            %
            (self.discIndex, self.path, self.movieName, cache, length))

        if queue:
            self._queueMovie()
        return True

    def findDisc(self, output):
        # Execute the info gathering
        # Save output into /tmp/ for interpreting 3 or 4 lines later
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

        if len(self.discIndex) == 0:
            print "No disc detected"
            return False
        else:
            print "Disc detected in drive %s" % self.discIndex
            return True

    def getTitle(self):
        self._cleanTitle()

        result = self.imdbScaper.search_movie(self.movieName, results=1)

        if len(result) > 0:
            self.movieName = result[0]

        return self.movieName
