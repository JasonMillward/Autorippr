MakeMKV and HandBrake Automater
===============================
[![githalytics.com alpha](https://cruel-carlota.pagodabox.com/00d3ea266eebd4aa375bb7d1019a9a0e "githalytics.com")](http://githalytics.com/JasonMillward/makeMKV-Autoripper)

This script uses [MakeMKV](http://makemkv.com/) to watch for DVDs or BDs that you own, grab the correct title from IMDb and rip it into your chosen movie directory and use [HandBrake](http://handbrake.fr/) to compress the video. All automagically.

***

### Prerequisites

Python (Obviously)
* Created using 2.7.3 but should work with similar versions

MakeMKV
* http://makemkv.com/

IMDbPy
* http://imdbpy.sourceforge.net/
    * At the time of writing, IMDbPy does not parse IMDb correctly because IMDb changed their HTML structure
    * sudo apt-get install python-imdbpy

Handbrake - For converting and compressing
* http://handbrake.fr/
    * sudo add-apt-repository ppa:stebbins/handbrake-releases
    * sudo apt-get update && sudo apt-get install handbrake-cli


### Installation

1. Install the above prerequisites manually or if you're using Ubuntu (and possibly other Debian based distros) a nice [setup script](https://github.com/JasonMillward/makeMKV-Autoripper/blob/master/setup/install.sh) has been included in the *setup* folder.
    * Originally created by [mechevar](http://www.makemkv.com/forum2/viewtopic.php?f=3&t=5266) but modified by me for easy install of all the required components.


2. Clone this repo into a directory of your chosing
    * ```git clone https://github.com/JasonMillward/makeMKV-Autoripper.git```


3. Check out a tagged *stable* release
    * To find available tags: ```git tag -l```
    * eg: ```git checkout v1.2```


4. Copy settings.blank.cfg to settings.cfg


5. Edit settings.cfg
    * You should only need to edit *save_path* unless you really want to play with the settings


### Running
1. Insert a DVD

2. Test script
    1. ```python ~/makeMKV-Autoripper/src/rip.py```
    2. ```python ~/makeMKV-Autoripper/src/encode.py```


3. Upon successful testing, set up a crontab and insert a new DVD
    * ```*/5     *       *       *       *       python ~/makeMKV-Autoripper/src/rip.py```
    * ```0       *       *       *       *       python ~/makeMKV-Autoripper/src/encode.py```


4. Procceed with whatever else you wanted to do today while casually changing discs


**NB**: If you have any issues with the script, head over to the [issues page](https://github.com/JasonMillward/makeMKV-Autoripper/issues), create a new issue with some information and hopefully a copy/paste of the error received.
