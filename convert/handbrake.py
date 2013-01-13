#!/usr/bin/env python

import os


class handbrake(object):

    def findProcess(self):
        processname = 'sleep'
        for line in os.popen("ps xa"):
            fields = line.split()
            pid = fields[0]
            process = fields[4]
            if process.find(processname) >= 0:
                print pid

    def loadMovie(self):
        self.home = os.path.expanduser("~")
        f = open("%s/.makemkvautoripper/queue" % self.home, "r")
        self.lines = f.readlines()
        f.close()
        self.movie = self.lines[0].replace("\n", "")

    def updateQueue(self):
        f = open("%s/.makemkvautoripper/queue" % self.home, "w")
        for line in self.lines:
            if line != self.movie + "\n":
                f.write(line)
        f.close()

    def convert():
        #HandBrakeCLI --verbose 1 --input "title00.mkv" --output "q21_ac3.mkv"
        print "Converting..."
