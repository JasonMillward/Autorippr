"""
Compression Wrapper


Released under the MIT license
Copyright (c) 2014, Ian Bird, Jason Millward

@category   misc
@version    $Id: 1.6.2, 2014-12-03 20:12:25 ACDT $;
@authors    Ian Bird, Jason Millward
@license    http://opensource.org/licenses/MIT
"""

import os

class Compression(object):
    def __init__(self, config):
        """
            Creates the required compression instances

            Inputs:
                config    (??): The configuration

            Outputs:
                The compression instance
        """
        self.log = logger.Logger("Compression", config['debug'])
        self.method = self.which_method(config)

    def which_method(self, config):
        if config['type'] == "ffmpeg":
            return ffmpeg.ffmpeg(config['debug'])
        else:
            return handbrake.handBrake(config['debug'], config['compression']['compressionPath'])

    def compress(self, **args):
        self.method.compress(**args)

    def check_exists(self, dbmovie):
        """
            Checks to see if the file still exists at the path set in the
                database

            Inputs:
                dbMovie (Obj): Movie database object

            Outputs:
                Bool    Does file exist

        """
        inmovie = "%s/%s" % (dbmovie.path, dbmovie.filename)

        if os.path.isfile(inmovie):
            return True

        else:
            self.log.debug(inmovie)
            self.log.error("Input file no longer exists")
            return False

    def cleanup(self, dbmovie):
        """
            Deletes files once the compression has finished with them

            Inputs:
                cFile    (Str): File path of the movie to remove

            Outputs:
                None
        """
        inmovie = "%s/%s" % (dbmovie.path, dbmovie.filename)

        try:
            os.remove(inmovie)
        except:
            self.log.error("Could not remove %s" % inmovie)
