"""
Configuration and requirements testing


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.6.1, 2014-08-18 10:42:00 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import sys
import os
import subprocess


def perform_testing(config):

    requirements = {
        "MakeMKV":   "makemkvcon",
        "Filebot":   "filebot",
        "HandBrake": "HandBrakeCLI",
        "FFmpeg (optional)": "ffmpeg"
    }

    print "= Checking directory permissions"
    print canWrite(config['makemkv']['savePath']), "makemkv savePath"

    print ""
    print "= Checking requirements"
    for req in requirements:
        print checkCommand(requirements[req]), req

    sys.exit(0)


def canWrite(path):
    try:
        ret = boolToStatus(os.access(path, os.W_OK | os.X_OK))
    except:
        ret = False
    finally:
        return ret


def boolToStatus(inBool):
    if inBool:
        return "[  OK  ]"
    else:
        return "[ FAIL ]"


def checkCommand(com):
    proc = subprocess.Popen(
        [
            'which',
            str(com)
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    return boolToStatus(len(proc.stdout.read()) > 0)
