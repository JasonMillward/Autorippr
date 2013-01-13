makeMKV-Autoripper
==================

This script uses [MakeMKV](http://makemkv.com/) to watch for and rip DVDs or BDs that you own automagically into their own directory.
It also looks up your discs title on IMDb to get the correct title before storing.

As an optional extra a converting script using [HandBrake](http://handbrake.fr/) has been included to compress movies to a reasonable size.

<hr>

## Additional Software
#### Required

Python (Obviously)
* Created using 2.7.3 but should work with similar versions

MakeMKV
* http://makemkv.com/

IMDbPy
* sudo apt-get install python-imdbpy

#### Optional

Handbrake - For converting and compressing
* http://handbrake.fr/
    * sudo add-apt-repository ppa:stebbins/handbrake-releases
    * sudo apt-get update && sudo apt-get install handbrake-cli

**Note:** For Ubuntu (and possibly other Debian based distros) a nice setup script has been included in the *setup* folder.
    Originally created by [mechevar](http://www.makemkv.com/forum2/viewtopic.php?f=3&t=5266) but modified by me for easy install of all the required components.