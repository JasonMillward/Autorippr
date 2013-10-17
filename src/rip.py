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
@version    $Id: 1.4, 2013-04-03 09:41:53 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT

Enough with these comments, on to the code
"""

import os
import sys
import ConfigParser
from makemkv import makeMKV
from timer import Timer

DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = "%s/../settings.cfg" % DIR


"""
    read_value temp doc
"""
def read_value(key):
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)
    to_return = config.get('MAKEMKV', key)
    config = None
    return to_return

"""
    rip temp doc string
"""
def rip():
    mkv_save_path = read_value('save_path')
    mkv_min_length = read_value('min_length')
    mkv_cache_size = read_value('cache_MB')
    mkv_tmp_output = read_value('temp_output')
    use_handbrake = read_value('handbrake')

    mkv_api = makeMKV()

    if (mkv_api.findDisc(mkv_tmp_output)):
        movie_title = mkv_api.getTitle()

        print movie_title
        sys.exit()

        if not os.path.exists('%s/%s' % (mkv_save_path, movie_title)):
            os.makedirs('%s/%s' % (mkv_save_path, movie_title))

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

        else:
            print "Movie folder already exists, will not overwrite."

    else:
        print "Could not find valid DVD in drive list"

if __name__ == '__main__':
    rip()
