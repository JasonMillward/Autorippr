"""
Auto Ripper

Ripping
    Uses MakeMKV to watch for movies inserted into DVD/BD Drives
    Looks up movie title on IMDb for saving into seperate directory

    Automaticly checks for existing directory/movie and will NOT overwrite existing
    files or folders
    Checks minimum length of video to ensure movie is ripped not previews or other
    junk that happens to be on the DVD

    DVD goes in > MakeMKV checks IMDb and gets a proper DVD name > MakeMKV Rips
    DVD does not get ejected, maybe it will get added to later versions

Compressing
    This script can be run with a simple cron, every hour should be fine

    An optional script used to rename and compress movies to an acceptable standard
    which still delivers quallity audio and video but reduces the file size
    dramatly.

    Using a nice value of 15 by default, it runs HandBrake as a background task
    that allows other critical tasks to complete first.

    Using this script with the auto ripper allows for multiple movies to be ripped
    and encoded with very little effot.


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT

Usage:
  autorip.py ( --rip | --compress | ( --rip --compress) ) [options]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --debug       Output debug.
  --rip         Rip disc using makeMKV.
  --compress    Compress using handbrake.

"""

import os
import ConfigParser
import yaml

from docopt import docopt
from logger import Logger
from timer import Timer
from tendo import singleton

__version__="1.6"

me = singleton.SingleInstance()
DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = "%s/settings.cfg" % DIR

def rip(config):
    """
        Main function for ripping
        Does everything
        Returns nothing
    """
    log = Logger("rip", config['debug'])

    mkv_save_path = config['save_path']
    mkv_tmp_output = config['temp_output']

    mkv_api = makeMKV(config)

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

def compress():
    """
    compress temp docstring
    """
    log = Logger("compress", read_value('debug'))

    hb_nice = int(read_value('nice'))
    hb_cli = read_value('com')
    hb_out = read_value('temp_output')

    hb_api = HandBrake(
        read_value('debug')
    )

    if hb_api.loadMovie():
        log.info( "Encoding and compressing %s" % hb_api.getMovieTitle()
        stopwatch = Timer()

        if hb_api.convert(args=hb_cli, nice=hb_nice, output=hb_out):
            log.info( "Movie was compressed and encoded successfully")

            stopwatch.stop()
            log.info( ("It took %s minutes to compress %s"
                %
                (stopwatch.getTime(), hb_api.getMovieTitle())))
        else:
            stopwatch.stop()
            log.info( "HandBrake did not complete successfully")
    else:
        log.info( "Queue does not exist or is empty")

if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    config = yaml.safe_load(open(CONFIG_FILE))

    if arguments['--rip']:
        rip(config['makemkv'])

    if arguments['--compress']:
        compress(config['handbrake'])
