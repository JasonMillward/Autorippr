"""
MakeMKV Auto Ripper

Uses MakeMKV to watch for movies inserted into DVD/BD Drives
Looks up movie title on IMDb for saving into seperate directory

Automaticly checks for existing directory/movie and will NOT overwrite existing
files or folders
Checks minimum length of video to ensure movie is ripped not previews or other
junk that happens to be on the DVD


This script can be run with a simple cron, every 5 minutes or so

DVD goes in > MakeMKV checks IMDb and gets a proper DVD name > MakeMKV Rips
DVD does not get ejected, maybe it will get added to later versions

Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT

Enough with these comments, on to the code
"""

import os
import ConfigParser
from makemkv import makeMKV
from logger import Logger
from timer import Timer

DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = "%s/../settings.cfg" % DIR


def read_value(key):
    """
        Reads the config file and returns the values

        Inputs:
            key         (Str)

        Outputs:
            to_return   (Str)
    """
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)
    to_return = config.get('MAKEMKV', key)
    config = None
    return to_return


def rip():
    """
        Main function for ripping
        Does everything
        Returns nothing
    """
    log = Logger("rip", read_value('debug'))

    mkv_save_path = read_value('save_path')
    mkv_tmp_output = read_value('temp_output')

    mkv_api = makeMKV(
        read_value('min_length'),
        read_value('cache_MB'),
        read_value('handbrake')
    )

    log.debug("Autoripper started successfully")
    log.debug("Checking for DVDs")

    dvds = mkv_api.findDisc(mkv_tmp_output)

    log.debug("%d DVDs found" % len(dvds))

    if (len(dvds) > 0):
        # Best naming convention ever
        for dvd in dvds:
            mkv_api.setTitle(dvd["discTitle"])
            mkv_api.setIndex(dvd["discIndex"])

            movie_title = mkv_api.getTitle()

            if not os.path.exists('%s/%s' % (mkv_save_path, movie_title)):
                os.makedirs('%s/%s' % (mkv_save_path, movie_title))

                mkv_api.getDiscInfo()

                stopwatch = Timer()

                if mkv_api.ripDisc(mkv_save_path, mkv_tmp_output):

                    stopwatch.stop()

                    log.info("It took %s minutes to complete the ripping of %s" %
                        (stopwatch.getTime(), movie_title)
                    )

                else:
                    stopwatch.stop()
                    log.info("MakeMKV did not did not complete successfully")
                    log.info("See log for more details")
                    log.debug("Movie title: %s" % movie_title)
            else:
                log.info("Movie folder %s already exists" % movie_title)

    else:
        log.info("Could not find any DVDs in drive list")

if __name__ == '__main__':
    rip()
