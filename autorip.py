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
    dramatically.

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
import sys
import yaml
from classes import *
from datetime import datetime
from tendo import singleton

__version__="1.6"

me = singleton.SingleInstance()
DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = "%s/settings.cfg" % DIR

def eject(drive):
    """
        Ejects the DVD drive
        Not really worth its own class
    """
    log = logger.logger("Eject", True)

    log.debug("Ejecting drive: " + drive)
    log.debug("Attempting OS detection")

    try:
        if sys.platform == 'win32':
            log.debug("OS detected as Windows")
            import ctypes
            ctypes.windll.winmm.mciSendStringW("set cdaudio door open", None, drive, None)

        elif sys.platform == 'darwin':
            log.debug("OS detected as OSX")
            p = os.popen("drutil eject " + drive)

            while 1:
                line = p.readline()
                if not line: break
                log.debug(line.strip())

        else:
            log.debug("OS detected as Unix")
            p = os.popen("eject -vr " + drive)

            while 1:
                line = p.readline()
                if not line: break
                log.debug(line.strip())

    except Exception as ex:
        log.error("Could not detect OS or eject CD tray")
        log.ex("An exception of type %s occured." % type(ex).__name__)
        log.ex("Args: \r\n %s" % ex.args)

    finally:
        del log

def rip(config):
    """
        Main function for ripping
        Does everything
        Returns nothing
    """
    log = logger.logger("Rip", config['debug'])

    mkv_save_path = config['makemkv']['savePath']
    mkv_tmp_output = config['makemkv']['temp']

    mkv_api = makemkv.makeMKV(config)

    log.debug("Ripping started successfully")
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

                Movies.create(
                    filename=movie_title,
                    path=mkv_save_path,
                    filebot=config['filebot']['enable'],
                    statusid=1,
                    lastupdated=datetime.now()
                )

                mkv_api.getDiscInfo()

                with stopwatch.stopwatch() as t:
                    status = mkv_api.ripDisc(mkv_save_path, mkv_tmp_output)

                if status:
                    if config['eject']:
                        eject(dvd['location'])

                    log.info("It took %s minute(s) to complete the ripping of %s" %
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

def compress(config):
    """
        Main function for compressing
        Does everything
        Returns nothing
    """
    log = logger.logger("Compress", config['debug'])

    hb = handbrake.handBrake(config['debug'])

    log.debug("Compressing started successfully")
    log.debug("Looking for movies to compress")

    if hb.loadMovie():
        log.info( "Compressing %s" % hb.getMovieTitle())

        with stopwatch.stopwatch() as t:
            convert = hb.convert(
                args=config['com'],
                nice=int(config['nice'])
            )

        if convert:
            log.info("Movie was compressed and encoded successfully")

            log.info( ("It took %s minutes to compress %s" %
                    (t.minutes, hb.getMovieTitle()))
            )
        else:
            log.info( "HandBrake did not complete successfully")

    else:
        log.info( "Queue does not exist or is empty")


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version=__version__)
    config = yaml.safe_load(open(CONFIG_FILE))
    config['debug'] = arguments['--debug']

    if arguments['--rip']:
        rip(config)

    if arguments['--compress']:
        compress(config)
