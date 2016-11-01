# -*- coding: utf-8 -*-
"""
MakeMKV CLI Wrapper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.7.0, 2016-08-22 14:53:29 ACST $;
@author     Jason Millward
@license    http://opensource.org/licenses/MIT
"""

import csv
import datetime
import re
import subprocess
import time

import logger

import utils


class MakeMKV(object):

    def __init__(self, config):
        self.discIndex = 0
        self.vidName = ""
        self.path = ""
        self.vidType = ""
        self.minLength = int(config['makemkv']['minLength'])
        self.maxLength = int(config['makemkv']['maxLength'])
        self.cacheSize = int(config['makemkv']['cache'])
        self.ignore_region = bool(config['makemkv']['ignore_region'])
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
        tmpname = self.vidName
        tmpname = tmpname.title().replace("Extended_Edition", "")
        tmpname = tmpname.replace("Special_Edition", "")
        tmpname = re.sub(r"Disc_(\d)(.*)", r"D\1", tmpname)
        tmpname = re.sub(r"Disc\s*(\d)(.*)", r"D\1", tmpname)
        tmpname = re.sub(r"Season_(\d)", r"S\1", tmpname)
        tmpname = re.sub(r"Season(\d)", r"S\1", tmpname)
        tmpname = re.sub(r"S(\d)_", r"S\1", tmpname)
        tmpname = tmpname.replace("_t00", "")
        tmpname = tmpname.replace("\"", "").replace("_", " ")

        # Clean up the edges and remove whitespace
        self.vidName = tmpname.strip()

    def _remove_duplicates(self, title_list):
        seen_titles = set()
        new_list = []
        for obj in title_list:
            if obj['title'] not in seen_titles:
                new_list.append(obj)
                seen_titles.add(obj['title'])

        return new_list

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

    def set_title(self, vidname):
        """
            Sets local video name

            Inputs:
                vidName   (Str): Name of video

            Outputs:
                None
        """
        self.vidName = vidname

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
                path    (Str):  Where the video will be saved to
                output  (Str):  Temp file to save output to

            Outputs:
                Success (Bool)
        """
        self.path = path

        fullpath = '%s/%s' % (self.path, self.vidName)

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
                "fail",
                "error"
            ]

            if any(x in line.lower() for x in badstrings):
                if self.ignore_region and "RPC protection" in line:
                    self.log.warn(line)
                elif "Failed to add angle" in line:
                    self.log.warn(line)
                else:
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

        foundtitles = int(self._read_mkv_messages("TCOUNT")[0])

        self.log.debug("MakeMKV found {} titles".format(foundtitles))

        if foundtitles > 0:
            for titleNo in set(self._read_mkv_messages("TINFO")):
                durTemp = self._read_mkv_messages("TINFO", titleNo, 9)[0]
                x = time.strptime(durTemp, '%H:%M:%S')
                titleDur = datetime.timedelta(
                    hours=x.tm_hour,
                    minutes=x.tm_min,
                    seconds=x.tm_sec
                ).total_seconds()

                if self.vidType == "tv" and titleDur > self.maxLength:
                    self.log.debug("Excluding Title No.: {}, Title: {}. Exceeds maxLength".format(
                        titleNo,
                        self._read_mkv_messages("TINFO", titleNo, 27)
                    ))
                    continue

                if self.vidType == "movie" and not re.search('00', self._read_mkv_messages("TINFO", titleNo, 27)[0]):
                    self.log.debug("Excluding Title No.: {}, Title: {}. Only want first title".format(
                        titleNo,
                        self._read_mkv_messages("TINFO", titleNo, 27)
                    ))
                    continue

                self.log.debug("MakeMKV title info: Disc Title: {}, Title No.: {}, Title: {}, ".format(
                    self._read_mkv_messages("CINFO", 2),
                    titleNo,
                    self._read_mkv_messages("TINFO", titleNo, 27)
                ))

                title = self._read_mkv_messages("TINFO", titleNo, 27)[0]
                rename_title = utils.strip_accents(title)
                rename_title = utils.clean_special_chars(rename_title)

                self.saveFiles.append({
                    'index': titleNo,
                    'title': title,
                    'rename_title': rename_title,
                })

    def get_type(self):
        """
            Returns the type of video (tv/movie)

            Inputs:
                None

            Outputs:
                vidType   (Str)
        """
        titlePattern = re.compile(
            r'(DISC_(\d))|(DISC(\d))|(D(\d))|(SEASON_(\d))|(SEASON(\d))|(S(\d))'
        )

        if titlePattern.search(self.vidName):
            self.log.debug("Detected TV {}".format(self.vidName))
            self.vidType = "tv"
        else:
            self.log.debug("Detected movie {}".format(self.vidName))
            self.vidType = "movie"
        return self.vidType

    def get_title(self):
        """
            Returns the current videos title

            Inputs:
                None

            Outputs:
                vidName   (Str)
        """
        self._clean_title()
        return self.vidName

    def get_savefiles(self):
        """
            Returns the current videos title

            Inputs:
                None

            Outputs:
                vidName   (Str)
        """
        return self._remove_duplicates(self.saveFiles)
