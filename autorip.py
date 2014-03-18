"""
Auto Ripper

Ripping
    Uses MakeMKV to watch for movies inserted into DVD/BD Drives

    Automaticly checks for existing directory/movie and will NOT overwrite existing
    files or folders

    Checks minimum length of video to ensure movie is ripped not previews or other
    junk that happens to be on the DVD

    DVD goes in > MakeMKV gets a proper DVD name > MakeMKV Rips
    DVD does not get ejected, maybe it will get added to later versions

Compressing
    An optional additional used to rename and compress movies to an acceptable standard
    which still delivers quallity audio and video but reduces the file size
    dramatly.

    Using a nice value of 15 by default, it runs HandBrake as a background task
    that allows other critical tasks to complete first.


Released under the MIT license
Copyright (c) 2014, Jason Millward

@category   misc
@version    $Id: 1.6, 2014-03-11 16:52:00 CST $;
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
    --test        Testing?

"""

import os
import yaml
from timer import timer
from tendo import singleton
from docopt import docopt
from logger import Logger
from makemkv import makeMKV

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
    log = Logger("Rip", config['debug'])

    mkv_save_path = config['savePath']
    mkv_tmp_output = config['temp']

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

                with timer() as t:
                    status = mkv_api.ripDisc(mkv_save_path, mkv_tmp_output)

                if status:
                    log.info("It took %s minutes to complete the ripping of %s" %
                        (t.minutes, movie_title)
                    )

                else:
                    log.info("MakeMKV did not did not complete successfully")
                    log.info("See log for more details")
                    log.debug("Movie title: %s" % movie_title)

            else:
                log.info("Movie folder %s already exists" % movie_title)

    else:
        log.info("Could not find any DVDs in drive list")

def compress(config, debug):
    """
    compress temp docstring
    """
    log = Logger("Compress", debug)

    hb_nice = int(config['nice'])
    hb_cli = config['com']
    hb_out = config['temp_output']

    hb_api = HandBrake(debug)

    if hb_api.loadMovie():
        log.info( "Encoding and compressing %s" % hb_api.getMovieTitle())

        if hb_api.convert(args=hb_cli, nice=hb_nice, output=hb_out):
            log.info( "Movie was compressed and encoded successfully")

            log.info( ("It took %s minutes to compress %s"
                %
                (stopwatch.getTime(), hb_api.getMovieTitle())))
        else:
            log.info( "HandBrake did not complete successfully")
    else:
        log.info( "Queue does not exist or is empty")


if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    config = yaml.safe_load(open(CONFIG_FILE))

    if arguments['--rip']:
        config['makemkv']['debug'] = arguments['--debug']
        rip(config['makemkv'])

    if arguments['--compress']:
        config['handbrake']['debug'] = arguments['--debug']
        compress(config['handbrake'])
