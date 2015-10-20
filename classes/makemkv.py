"""
MakeMKV CLI Wrapper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.7-test2, 2015-05-11 07:48:38 ACST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import subprocess
import os
import re
import csv
import logger
import datetime
import time


class MakeMKV(object):

    def __init__(self, config):
        self.discIndex = 0
        self.movieName = ""
        self.path = ""
        self.minLength = int(config['makemkv']['minLength'])
        self.maxLength = int(config['makemkv']['maxLength'])
        self.cacheSize = int(config['makemkv']['cache'])
        self.log = logger.Logger("Makemkv", config['debug'], config['silent'])
        self.makemkvconPath = config['makemkv']['makemkvconPath']
        self.saveFiles = []

    def _clean_title(self):
        """
            Removes the extra bits in the title and removes whitespace

            Inputs:
                None

            Outputs:
                None
        """
        tmpname = self.movieName
        tmpname = tmpname.title().replace("Extended_Edition", "")
        tmpname = tmpname.replace("Special_Edition", "")
        tmpname = re.sub(r"Disc_(\d)", r"D\1", tmpname)
        tmpname = re.sub(r"Disc(\d)", r"D\1", tmpname)
        tmpname = re.sub(r"Season_(\d)", r"S\1", tmpname)
        tmpname = re.sub(r"Season(\d)", r"S\1", tmpname)
        tmpname = re.sub(r"S(\d)_", r"S\1", tmpname)
        tmpname = tmpname.replace("_t00", "")
        tmpname = tmpname.replace("\"", "").replace("_", " ")

        # Clean up the edges and remove whitespace
        self.movieName = tmpname.strip()

    def _read_mkv_messages(self, stype, sid=None, scode=None):
        """
            Returns a list of messages that match the search string
            Parses message output.

            Inputs:
                stype   (Str): Type of message
                sid     (Int): ID of message
                scode   (Int): Code of message

            Outputs:
                toreturn    (List)
        """
        toreturn = []

        with open('/tmp/makemkvMessages', 'r') as messages:
            for line in messages:
                if line[:len(stype)] == stype:
                    values = line.replace("%s:" % stype, "").strip()

                    cr = csv.reader([values])

                    if sid is not None:
                        for row in cr:
                            if int(row[0]) == int(sid):
                                if scode is not None:
                                    if int(row[1]) == int(scode):
                                        toreturn.append(row[3])
                                else:
                                    toreturn.append(row[2])

                    else:
                        for row in cr:
                            toreturn.append(row[0])

        return toreturn

    def set_title(self, moviename):
        """
            Sets local movie name

            Inputs:
                movieName   (Str): Name of movie

            Outputs:
                None
        """
        self.movieName = moviename

    def set_index(self, index):
        """
            Sets local disc index

            Inputs:
                index   (Int): Disc index

            Outputs:
                None
        """
        self.discIndex = int(index)

    def rip_disc(self, path, titleIndex):
        """
            Passes in all of the arguments to makemkvcon to start the ripping
                of the currently inserted DVD or BD

            Inputs:
                path    (Str):  Where the movie will be saved to
                output  (Str):  Temp file to save output to

            Outputs:
                Success (Bool)
        """
        self.path = path

        fullpath = '%s/%s' % (self.path, self.movieName)

        proc = subprocess.Popen(
            [
                '%smakemkvcon' % self.makemkvconPath,
                'mkv',
                'disc:%d' % self.discIndex,
                titleIndex,
                fullpath,
                '--cache=%d' % self.cacheSize,
                '--noscan',
                '--minlength=%d' % self.minLength
            ],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        (results, errors) = proc.communicate()

        if proc.returncode is not 0:
            self.log.error(
                "MakeMKV (rip_disc) returned status code: %d" % proc.returncode)

        if errors is not None:
            if len(errors) is not 0:
                self.log.error("MakeMKV encountered the following error: ")
                self.log.error(errors)
                return False

        checks = 0

        lines = results.split("\n")
        for line in lines:
            if "skipped" in line:
                continue

            badstrings = [
                "failed",
                "Fail",
                "error"
            ]

            if any(x in line.lower() for x in badstrings):
                self.log.error(line)
                return False

            if "Copy complete" in line:
                checks += 1

            if "titles saved" in line:
                checks += 1

        if checks >= 2:
            return True
        else:
            return False

    def find_disc(self):
        """
            Use makemkvcon to list all DVDs or BDs inserted
            If more then one disc is inserted, use the first result

            Inputs:
                output  (Str): Temp file to save output to

            Outputs:
                Success (Bool)
        """
        drives = []
        proc = subprocess.Popen(
            ['%smakemkvcon' % self.makemkvconPath, '-r', 'info', 'disc:-1'],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        (results, errors) = proc.communicate()

        if proc.returncode is not 0:
            self.log.error(
                "MakeMKV (find_disc) returned status code: %d" % proc.returncode)

        if errors is not None:
            if len(errors) is not 0:
                self.log.error("MakeMKV encountered the following error: ")
                self.log.error(errors)
                return []

        if "This application version is too old." in results:
            self.log.error("Your MakeMKV version is too old."
                           "Please download the latest version at http://www.makemkv.com"
                           " or enter a registration key to continue using MakeMKV.")

            return []

        # Passed the simple tests, now check for disk drives
        lines = results.split("\n")
        for line in lines:
            if line[:4] == "DRV:":
                if "/dev/" in line:
                    out = line.split(',')

                    if len(str(out[5])) > 3:

                        drives.append(
                            {
                                "discIndex": out[0].replace("DRV:", ""),
                                "discTitle": out[5],
                                "location": out[6]
                            }
                        )

        return drives

    def get_disc_info(self):
        """
            Returns information about the selected disc

            Inputs:
                None

            Outputs:
                None
        """

        proc = subprocess.Popen(
            [
                '%smakemkvcon' % self.makemkvconPath,
                '-r',
                'info',
                'disc:%d' % self.discIndex,
                '--minlength=%d' % self.minLength,
                '--messages=/tmp/makemkvMessages'
            ],
            stderr=subprocess.PIPE
        )

        (results, errors) = proc.communicate()

        if proc.returncode is not 0:
            self.log.error(
                "MakeMKV (get_disc_info) returned status code: %d" % proc.returncode)

        if errors is not None:
            if len(errors) is not 0:
                self.log.error("MakeMKV encountered the following error: ")
                self.log.error(errors)
                return False

        foundtitles = int( self._read_mkv_messages("TCOUNT")[0] )

        self.log.debug("MakeMKV found {} titles".format( foundtitles ))

        if foundtitles > 0:
            for titleNo in set(self._read_mkv_messages("TINFO")):
                durTemp = self._read_mkv_messages("TINFO", titleNo, 9)[0]
                x = time.strptime(durTemp,'%H:%M:%S')
                titleDur = datetime.timedelta(
                    hours=x.tm_hour,
                    minutes=x.tm_min,
                    seconds=x.tm_sec
                ).total_seconds()
                if foundtitles > 1 and titleDur > self.maxLength:
                    self.log.debug( "Excluding Title No.: {}, Title: {}. Exceeds maxLength".format(
                        titleNo,
                        self._read_mkv_messages("TINFO", titleNo, 27)
                    ))                    
                    continue
                self.log.debug( "MakeMKV title info: Disc Title: {}, Title No.: {}, Title: {}, ".format(
                    self._read_mkv_messages("CINFO", 2),
                    titleNo,
                    self._read_mkv_messages("TINFO", titleNo, 27)
                ))

                title = self._read_mkv_messages("TINFO", titleNo, 27)[0]

                self.saveFiles.append({
                    'index': titleNo,
                    'title': title
                })
        else:
           pass 

    def get_title(self):
        """
            Returns the current movies title

            Inputs:
                None

            Outputs:
                movieName   (Str)
        """
        self._clean_title()
        return self.movieName

    def get_savefiles(self):
        """
            Returns the current movies title

            Inputs:
                None

            Outputs:
                movieName   (Str)
        """
        return self.saveFiles
