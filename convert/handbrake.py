#!/usr/bin/env python

import os
import commands


class handbrake(object):

    def findProcess(self):
        processname = 'HandBrakeCLI'
        for line in os.popen("ps xa"):
            fields = line.split()
            process = fields[4]
            if process.find(processname) >= 0:
                return True
                break

        return False

    def loadMovie(self):
        self.home = os.path.expanduser("~")
        if os.path.isfile("%s/.makemkvautoripper/queue" % self.home):
            f = open("%s/.makemkvautoripper/queue" % self.home, "r")
            self.lines = f.readlines()
            f.close()
            movie = self.lines[0].replace("\n", "")
            movie.split('|')
            self.inputFile = movie[0]
            self.outputFile = movie[1]

            return True
        else:
            return False

    def updateQueue(self):
        f = open("%s/.makemkvautoripper/queue" % self.home, "w")
        for line in self.lines:
            if line != self.movie + "\n":
                f.write(line)
        f.close()

    def convert(self, args):
        commands.getstatusoutput(
            'HandBrakeCLI --verbose 1 --input "%s" --output "%s" %s'
            %
            (self.inputFile, self.outputFile, args))

        print "Converting..."

