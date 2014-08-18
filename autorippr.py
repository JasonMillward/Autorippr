"""
Autorippr

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

Extras


Released under the MIT license
Copyright (c) 2014, Jason Millward

@category   misc
@version    $Id: 1.6, 2014-07-21 18:48:00 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT

Usage:
    autorippr.py   ( --rip | --compress | --extra )  [options]
    autorippr.py   ( --rip [ --compress ] )          [options]
    autorippr.py   --all                             [options]
    autorippr.py   --test

Options:
    -h --help       Show this screen.
    --version       Show version.
    --debug         Output debug.
    --rip           Rip disc using makeMKV.
    --compress      Compress using HandBrake.
    --extra         Lookup, rename and/or download extras.
    --all           Do everything
    --test          Tests config and requirements

"""

import os
import sys
import yaml
import subprocess
from classes import *
from tendo import singleton

__version__ = "1.6.1"

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
            ctypes.windll.winmm.mciSendStringW(
                "set cdaudio door open", None, drive, None)

        elif sys.platform == 'darwin':
            log.debug("OS detected as OSX")
            p = os.popen("drutil eject " + drive)

            while 1:
                line = p.readline()
                if not line:
                    break
                log.debug(line.strip())

        else:
            log.debug("OS detected as Unix")
            p = os.popen("eject -vm " + drive)

            while 1:
                line = p.readline()
                if not line:
                    break
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

    log.debug("Ripping initialised")
    mkv_api = makemkv.makeMKV(config)

    log.debug("Checking for DVDs")
    dvds = mkv_api.find_disc()

    log.debug("%d DVDs found" % len(dvds))

    if (len(dvds) > 0):
        # Best naming convention ever
        for dvd in dvds:
            mkv_api.set_title(dvd["discTitle"])
            mkv_api.set_index(dvd["discIndex"])

            movie_title = mkv_api.get_title()

            movie_path = '%s/%s' % (mkv_save_path, movie_title)
            if not os.path.exists(movie_path):
                os.makedirs(movie_path)

                dbMovie = database.insert_movie(
                    movie_title,
                    movie_path,
                    config['filebot']['enable']
                )

                database.insert_history(
                    dbMovie,
                    "Movie added to database"
                )

                mkv_api.get_disc_info()

                database.update_movie(dbMovie, 3, mkv_api.get_savefile())

                with stopwatch.stopwatch() as t:
                    database.insert_history(
                        dbMovie,
                        "Movie submitted to MakeMKV"
                    )
                    status = mkv_api.rip_disc(mkv_save_path)

                if status:
                    if config['makemkv']['eject']:
                        eject(dvd['location'])

                    log.info("It took %s minute(s) to complete the ripping of %s" %
                             (t.minutes, movie_title)
                             )

                    database.update_movie(dbMovie, 4)

                else:
                    log.info("MakeMKV did not did not complete successfully")
                    log.info("See log for more details")
                    log.debug("Movie title: %s" % movie_title)

                    database.insert_history(
                        dbMovie,
                        "MakeMKV failed to rip movie"
                    )

                    database.update_movie(dbMovie, 2)

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

    log.debug("Compressing initialised")
    log.debug("Looking for movies to compress")

    dbMovie = database.next_movie_to_compress()

    if dbMovie is not None:
        if hb.check_exists(dbMovie) is not False:

            database.update_movie(dbMovie, 5)

            log.info("Compressing %s" % dbMovie.moviename)

            with stopwatch.stopwatch() as t:
                status = hb.compress(
                    args=config['handbrake']['com'],
                    nice=int(config['handbrake']['nice']),
                    dbMovie=dbMovie
                )

            if status:
                log.info("Movie was compressed and encoded successfully")

                log.info(("It took %s minutes to compress %s" %
                          (t.minutes, dbMovie.moviename))
                         )

                database.insert_history(
                    dbMovie,
                    "HandBake Completed successfully"
                )

                database.update_movie(
                    dbMovie, 6, filename="%s.mkv" % dbMovie.moviename)

            else:
                database.update_movie(dbMovie, 5)

                database.insert_history(dbMovie, "Handbrake failed", 4)

                log.info("HandBrake did not complete successfully")
        else:
            database.update_movie(dbMovie, 2)

            database.insert_history(
                dbMovie, "Input file no longer exists", 4
            )

    else:
        log.info("Queue does not exist or is empty")


def extras(config):
    """
        Main function for filebotting
        Does everything
        Returns nothing
    """
    log = logger.logger("Extras", config['debug'])

    fb = filebot.filebot(config['debug'])

    dbMovie = database.next_movie_to_filebot()

    if dbMovie is not None:
        log.info("Attempting movie rename")

        database.update_movie(dbMovie, 7)

        status = fb.rename(dbMovie)

        if status[0]:
            log.info("Rename success")
            database.update_movie(dbMovie, 6, filename=status[1])

            if config['filebot']['subtitles']:
                log.info("Grabbing subtitles")

                status = fb.get_subtitles(
                    dbMovie, config['filebot']['language'])

                if status:
                    log.info("Subtitles downloaded")
                    database.update_movie(dbMovie, 8)

                else:
                    log.info("Subtitles not downloaded, no match")
                    database.update_movie(dbMovie, 8)

                log.info("Completed work on %s" % dbMovie.moviename)

                if config['commands'] is not None and len(config['commands']) > 0:
                    for com in config['commands']:
                        proc = subprocess.Popen(
                            [com],
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            shell=True
                        )

            else:
                log.info("Not grabbing subtitles")
                database.update_movie(dbMovie, 8)

        else:
            log.info("Rename failed")

    else:
        log.info("No movies ready for filebot")


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version=__version__)
    config = yaml.safe_load(open(CONFIG_FILE))

    config['debug'] = arguments['--debug']

    if bool(config['analytics']['enable']):
        analytics.ping(__version__)

    if arguments['--test']:
        testing.perform_testing(config)

    if arguments['--rip'] or arguments['--all']:
        rip(config)

    if arguments['--compress'] or arguments['--all']:
        compress(config)

    if arguments['--extra'] or arguments['--all']:
        extras(config)
