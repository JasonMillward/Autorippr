#!/usr/bin/python
#HandBrakeCLI --verbose 1 --input "title00.mkv" --output "q21_ac3.mkv"

import os

home = os.path.expanduser("~")

f = open("%s/.makemkvautoripper/queue" % home, "r")
lines = f.readlines()
f.close()

movie = lines[0].replace("\n", "")

f = open("%s/.makemkvautoripper/queue" % home, "w")
for line in lines:
    if line != movie + "\n":
        f.write(line)
f.close()
