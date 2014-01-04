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
    mkv_save_path = read_value('save_path')
    mkv_min_length = int(read_value('min_length'))
    mkv_cache_size = int(read_value('cache_MB'))
    mkv_tmp_output = read_value('temp_output')
    use_handbrake = bool(read_value('handbrake'))

    mkv_api = makeMKV()

    dvds = mkv_api.findDisc(mkv_tmp_output)

    if (len(dvds) > 0):
        # Best naming convention ever
        for dvd in dvds:
            mkv_api.setTitle(dvd["discTitle"])
            mkv_api.setIndex(dvd["discIndex"])

            if not os.path.exists('%s/%s' % (mkv_save_path, dvd["discTitle"])):
                os.makedirs('%s/%s' % (mkv_save_path, dvd["discTitle"]))

                movie_title = mkv_api.getTitle()

                """
                stopwatch = Timer()

                if mkv_api.ripDisc(path=mkv_save_path,
                        length=mkv_min_length,
                        cache=mkv_cache_size,
                        queue=use_handbrake,
                        output=mkv_tmp_output):

                    stopwatch.stop()

                    print ("It took %s minutes to complete the ripping of %s"
                        %
                        (stopwatch.getTime(), movie_title))

                else:
                    stopwatch.stop()
                    print "MakeMKV did not did not complete successfully"
                    print "Movie title: %s" % movie_title
                """
            else:
                print "Movie folder %s already exists" % movie_title

    else:
        print "Could not find any DVDs in drive list"

if __name__ == '__main__':
    rip()
