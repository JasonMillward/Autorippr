#!/usr/bin/env python

import commands
import imdb
import os


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

        with open("%s/.makemkvautoripper/queue" % home, "a+") as myfile:
            myfile.write("%s/%s/%s|%s/%s" % (self.path, self.movieName, movie, self.path, self.movieName))

                #print files
                #os.rename(files, "%s.mkv" % movieName)

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

        # Check to see if there is a disc in the system
        #
        # For every line in the output
        # If the first 4 characters are DRV:
        #   Check to see if a device is specified
        #       If so, get the 1st and 6th element of the array

        for line in tempFile.readlines():
            if line[:4] == "DRV:":
                if "/dev/" in line:
                    drive = line.split(',')
                    self.discIndex = drive[0].replace("DRV:", "")
                    self.movieName = drive[5]

        # If there was no disc, exit
        if len(self.discIndex) == 0:
            print "No disc detected"
            return False
        else:
            print "Disc detected in drive %s" % self.discIndex
            return True

    def getTitle(self):
        # A little fix for extended editions (eg; Die Hard 4)
        self.movieName = self.movieName.title().replace("Extended_Edition", "")

        # Clean up the disc title so IMDb can identify it easier
        self.movieName = self.movieName.replace("\"", "").replace("_", " ")

        # Get the closest 2 results, do nothing with the other 1
        result = self.imdbScaper.search_movie(self.movieName, results=2)

        # If the returned result is not empty, save it, otherwise IMDb can't
        #   identify the DVD
        if len(result) > 0:
            self.movieName = result[0]

        return self.movieName
