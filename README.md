MakeMKV and HandBrake Automater
===============================
[![githalytics.com alpha](https://cruel-carlota.pagodabox.com/00d3ea266eebd4aa375bb7d1019a9a0e "githalytics.com")](http://githalytics.com/JasonMillward/makeMKV-Autoripper)

This script uses [MakeMKV](http://makemkv.com/) to watch for DVDs or BDs that you own, grab the correct title from IMDb and rip it into your chosen movie directory and use [HandBrake](http://handbrake.fr/) to compress the video. All automagically.
***

### Prerequisites

Python
* Created using 2.7.3 but should work with similar versions

MakeMKV
* http://makemkv.com/

Handbrake - For converting and compressing
* http://handbrake.fr/

### Installation

1. Install prerequisites 

2. Clone this repo into a directory of your chosing
    * ```git clone https://github.com/JasonMillward/makeMKV-Autoripper.git```


3. Check out a tagged *stable* release
    * To find available tags: ```git tag -l```
    * eg: ```git checkout v1.3```

4. Edit settings.cfg
    * You should only need to edit *save_path* unless you really want to play with the settings


### Running
1. Insert a DVD

2. Test script
    1. ```makeMKV-Autoripper/src$ python autorip.py --rip```
    2. ```makeMKV-Autoripper/src$ python autorip.py --compress```


3. Upon successful testing, set up a crontab and insert a new DVD
    * ```*/5     *       *       *       *       python ~/makeMKV-Autoripper/src/autorip.py --rip```
    * ```0       *       *       *       *       python ~/makeMKV-Autoripper/src/autorip.py --compress```


4. Procceed with whatever else you wanted to do today while casually changing discs


### Issues


If you have any issues with the script, head over to the [issues page](https://github.com/JasonMillward/makeMKV-Autoripper/issues), create a new issue.

Please try to supply as much detail as possible about the issue you are having, including but not limited to:
* If you are ripping a DVD or Blu-ray 
* If you are using handbrake and/or makemkv
* The error received 
* A copy (or relevant section) of autoripper.log 
* Your operating system

An easy way to get some of the information required:  
```curl https://raw.github.com/KittyKatt/screenFetch/master/screenfetch-dev | bash```

