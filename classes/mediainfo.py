# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 11:20:23 2017

Dependencies:
   System:
       mediainfo
       mkvtoolnix

   Python (nonstandard library):
       pymediainfo

For Windows, if mediainfo or mkvpropedit aren't in PATH, must give path to .dll (mediainfo)
or .exe (mkvpropedit) file
For *nixs, use path to binary (although it's likly in PATH)

Takes an mkv file and analyzes it for foreign subtitle track. Assumes that foreign subtitle
track files are smaller in bit size but the same length as the main language track


@author: brodi
"""

import os
from pymediainfo import MediaInfo
from pipes import quote
import logger
import shlex
import subprocess

# main class that initializes settings for discovering/flagging a forced subtitle track
# edits python's os.environ in favor of putting full string when calling executables
class ForcedSubs(object):
    def __init__(self, config):
        self.log = logger.Logger('ForcedSubs', config['debug'], config['silent'])
        self.lang = config['ForcedSubs']['language']
        self.secsub_ratio = float(config['ForcedSubs']['ratio'])
        self.mediainfoPath = config['ForcedSubs']['mediainfoPath']
        self.mkvpropeditPath = config['ForcedSubs']['mkvpropeditPath']
        if (self.mediainfoPath and
            os.path.dirname(self.mediainfoPath) not in os.environ['PATH']):
            os.environ['PATH'] = (os.path.dirname(config['ForcedSubs']['mediainfoPath']) + ';' +
                                  os.environ['PATH'])
        if (self.mkvpropeditPath and
            os.path.dirname(self.mkvpropeditPath) not in os.environ['PATH']):
            os.environ['PATH'] = (os.path.dirname(config['ForcedSubs']['mkvpropeditPath']) + ';' +
                                  os.environ['PATH'])

    def discover_forcedsubs(self, dbvideo):
        """
            Attempts to find foreign subtitle track

            Input:
                dbvideo (Obj): Video database object

            Output:
                If successful, track number of forced subtitle
                Else, None
        """
        MEDIADIR = os.path.join(dbvideo.path, dbvideo.filename)
#        wrapper class for mediainfo tool
        media_info = MediaInfo.parse(MEDIADIR.encode('unicode-escape'))
        subs = []
#       Iterates though tracks and finds subtitles in preferred language, creates
#       list of dictionaries
        for track in media_info.tracks:
            data = track.to_data()
            if data['track_type'] == 'Text' and data['language']==self.lang:
                subs.append(data)
        if len(subs) is 0:
            self.log.info("No subtitle found, cannot determine foreign language track.")
            return None
        if len(subs) is 1:
            self.log.info("Only one {} subtitle found, cannot determine foreign language track."
                          .format(self.lang))
            return None

#   Sort list by size of track file
        subs.sort(key=lambda sub: sub['stream_size'], reverse = True)

#   Main language subtitle assumed to be largest
        main_sub = subs[0]
        main_subsize = main_sub['stream_size']
        main_sublen = float(main_sub['duration'])
#   Checks other subs for size, duration, and if forced flag is set
        for sub in subs[1:]:
            if (
                sub['stream_size'] <= main_subsize*self.secsub_ratio
                and main_sublen*.9 <= float(sub['duration']) <= main_sublen*1.1
                and sub['forced']=='No'
                ):
                secondary_sub = sub
            else:
                self.log.info("No foreign language subtitle found, try adjusting ratio.")
                return None
        return secondary_sub['track_id']

    def flag_forced(self, dbvideo, track):
        """
            Uses mkvpropedit to edit mkv header and flag the detected track as 'forced'

            Input:
                dbvideo (Obj): Video database object
                track (int): Track number of foreign track to be flagged as 'forced'

            Output:
                Bool: Returns True of successful, returns False if not
        """

        MEDIADIR = os.path.join(dbvideo.path, dbvideo.filename)
        cmd_raw = 'mkvpropedit {} --edit track:{} --set flag-forced=1'.format(quote(MEDIADIR), track)
        cmd = shlex.split(cmd_raw)
        self.log.debug("mkpropedit cmd: {}".format(cmd))

        proc = subprocess.Popen(
                                cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE
                                )
        
        (results, error) = proc.communicate()


        if proc.returncode is not 0:
            self.log.error(
                           "mkvpropedit (forced subtitles) returned status code {}".format(proc.returncode)
                           )
            return False

        if len(results) is not 0:
            lines = results.split('\n')
            for line in lines:
                self.log.debug(line.strip())

        return True

