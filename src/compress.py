"""
HandBrake queue parser

Uses HandBrake to compress movies ripped by makeMKV


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
"""

import os
import ConfigParser
from handbrake import HandBrake
from timer import Timer
from tendo import singleton

me = singleton.SingleInstance()
DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = "%s/../settings.cfg" % DIR

def read_value(key):
    """
    read_value temp docstring
    """
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)
    to_return = config.get('HANDBRAKE', key)
    config = None
    return to_return


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

    if not hb_api.findProcess():
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
    else:
        log.info( "Process already running skipper")

if __name__ == '__main__':
    compress()
