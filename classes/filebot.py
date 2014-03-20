"""
FileBot class


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import os
import subprocess
import database
import logger


class filebot(object):

    def __init__(self, debug):
        self.db = database.database()
        self.log = logger.logger("Filebot", debug)

    # Filebots order of instructions should be
    # Rename
    #   filebot -rename title00.mkv --q [Movie Name] -non-strict
    #
    # get subtitles
    #   filebot -get-missing-subtitles --lang