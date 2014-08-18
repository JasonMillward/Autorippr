"""
MakeMKV CLI Wrapper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.6.1, 2014-08-18 10:42:00 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

import subprocess
import os
import re
import csv
import logger


class makeMKV(object):

    def __init__(self, config):
        self.discIndex = 0
        self.movieName = ""
        self.path = ""
        self.movieName = ""
        self.minLength = int(config['makemkv']['minLength'])
        self.cacheSize = int(config['makemkv']['cache'])
        self.log = logger.logger("Makemkv", config['debug'])

    def _clean_title(self):
        """
            Removes the extra bits in the title and removes whitespace

            Inputs:
                None

            Outputs:
                None
        """
        tmpName = self.movieName

        tmpName = tmpName.title().replace("Extended_Edition", "")

        tmpName = tmpName.replace("Special_Edition", "")

        tmpName = re.sub(r"Disc_(\d)", "", tmpName)

        tmpName = tmpName.replace("_t00", "")

        tmpName = tmpName.replace("\"", "").replace("_", " ")

        # Clean up the edges and remove whitespace
        self.movieName = tmpName.strip()

    def _read_MKV_messages(self, stype, sid=None, scode=None):
        """
            Returns a list of messages that match the search string
            Parses message output.

            Inputs:
                stype   (Str): Type of message
                sid     (Int): ID of message
                scode   (Int): Code of message

            Outputs:
                toReturn    (List)
        """
        toReturn = []

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
                                        toReturn.append(row[3])
                                else:
                                    toReturn.append(row[2])

                    else:
                        for row in cr:
                            toReturn.append(row[0])

        return toReturn

    def set_title(self, movieName):
        """
            Sets local movie name

            Inputs:
                movieName   (Str): Name of movie

            Outputs:
                None
        """
        self.movieName = movieName

    def set_index(self, index):
        """
            Sets local disc index

            Inputs:
                index   (Int): Disc index

            Outputs:
                None
        """
        self.discIndex = int(index)

    def rip_disc(self, path):
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

        fullPath = '%s/%s' % (self.path, self.movieName)

        proc = subprocess.Popen(
            [
                'makemkvcon',
                'mkv',
                'disc:%d' % self.discIndex,
                '0',
                fullPath,
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

            badStrings = [
                "failed",
                "Fail",
                "error"
            ]

            if any(x in line.lower() for x in badStrings):
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
            ['makemkvcon', '-r', 'info', 'disc:-1'],
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
                'makemkvcon',
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

        self.log.debug("MakeMKV found %d titles" %
                       len(self._read_MKV_messages("TCOUNT")))
        for titleNo in set(self._read_MKV_messages("TINFO")):
            self.log.debug("Title number: %s" % titleNo)

            self.log.debug(self._read_MKV_messages("CINFO", 2))

            self.saveFile = self._read_MKV_messages("TINFO", titleNo, 27)
            self.saveFile = self.saveFile[0]

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

    def get_savefile(self):
        """
            Returns the current movies title

            Inputs:
                None

            Outputs:
                movieName   (Str)
        """
        return self.saveFile
