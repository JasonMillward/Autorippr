"""
Compression Wrapper


Released under the MIT license
Copyright (c) 2014, Ian Bird, Jason Millward

@category   misc
@version    $Id: 1.7-test2, 2015-05-11 07:48:38 ACST $;
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
        self.log = logger.Logger("Compression", config[
                                 'debug'], config['silent'])
        self.method = self.which_method(config)
        self.invid = ""

    def which_method(self, config):
        if config['compress']['type'] == "ffmpeg":
            return ffmpeg.FFmpeg(config['debug'], config['silent'], config['compress']['format'])
        else:
            return handbrake.HandBrake(config['debug'], config['compress']['compressionPath'], config['compress']['format'], config['silent'])

    def compress(self, **args):
        return self.method.compress(**args)

    def check_exists(self, dbvideo):
        """
            Checks to see if the file still exists at the path set in the
                database

            Inputs:
                dbvideo (Obj): Video database object

            Outputs:
                Bool    Does file exist

        """
        self.invid = "%s/%s" % (dbvideo.path, dbvideo.filename)

        if os.path.isfile(self.invid):
            return True

        else:
            self.log.debug(self.invid)
            self.log.error("Input file no longer exists")
            return False

    def cleanup(self):
        """
            Deletes files once the compression has finished with them

            Inputs:
                cFile    (Str): File path of the video to remove

            Outputs:
                None
        """
        if self.invid is not "":
            try:
                os.remove(self.invid)
            except:
                self.log.error("Could not remove %s" % self.invid)
