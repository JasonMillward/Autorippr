"""
FFmpeg Wrapper


Released under the MIT license
Copyright (c) 2014, Ian Bird

@category   misc
@version    $Id: 1.6.2, 2014-12-03 20:12:25 ACDT $;
@author     Ian Bird
@license    http://opensource.org/licenses/MIT
"""

import os

def create(config):
    """
        Creates the required compression instances

        Inputs:
            config    (??): The configuration

        Outputs:
            The compression instance
    """
    if config['type'] == "ffmpeg":
        return ffmpeg.ffmpeg(config['debug'])
    else:
        return handbrake.handBrake(config['debug'], config['compression']['compressionPath']);

class compression(object):

    def check_exists(self, dbMovie):
        """
            Checks to see if the file still exists at the path set in the
                database

            Inputs:
                dbMovie (Obj): Movie database object

            Outputs:
                Bool    Does file exist

        """
        inMovie = "%s/%s" % (dbMovie.path, dbMovie.filename)

        if os.path.isfile(inMovie):
            return True

        else:
            self.log.debug(inMovie)
            self.log.error("Input file no longer exists")
            return False

    def _cleanUp(self, cFile):
        """
            Deletes files once the compression has finished with them

            Inputs:
                cFile    (Str): File path of the movie to remove

            Outputs:
                None
        """
        try:
            os.remove(cFile)
        except:
            self.log.error("Could not remove %s" % cFile)
