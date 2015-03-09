"""
Compression Wrapper


Released under the MIT license
Copyright (c) 2014, Ian Bird, Jason Millward

@category   misc
@version    $Id: 1.7-testing, 2015-03-09 21:25:58 ACDT $;
@authors    Ian Bird, Jason Millward
@license    http://opensource.org/licenses/MIT
"""

import os
import logger
import handbrake
import ffmpeg

class Compression(object):
    def __init__(self, config):
        """
            Creates the required compression instances

            Inputs:
                config    (??): The configuration

            Outputs:
                The compression instance
        """
        self.log = logger.Logger("Compression", config['debug'], config['silent'])
        self.method = self.which_method(config)
        self.inmovie = ""

    def which_method(self, config):
        if config['compress']['type'] == "ffmpeg":
            return ffmpeg.FFmpeg(config['debug'], config['silent'])
        else:
            return handbrake.HandBrake(config['debug'], config['compress']['compressionPath'], config['silent'])

    def compress(self, **args):
        return self.method.compress(**args)

    def check_exists(self, dbmovie):
        """
            Checks to see if the file still exists at the path set in the
                database

            Inputs:
                dbMovie (Obj): Movie database object

            Outputs:
                Bool    Does file exist

        """
        self.inmovie = "%s/%s" % (dbmovie.path, dbmovie.filename)

        if os.path.isfile(self.inmovie):
            return True

        else:
            self.log.debug(self.inmovie)
            self.log.error("Input file no longer exists")
            return False

    def cleanup(self):
        """
            Deletes files once the compression has finished with them

            Inputs:
                cFile    (Str): File path of the movie to remove

            Outputs:
                None
        """
        if self.inmovie is not "":
            try:
                os.remove(self.inmovie)
            except:
                self.log.error("Could not remove %s" % self.inmovie)

