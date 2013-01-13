makeMKV-Autoripper
==================

This script uses [MakeMKV](http://makemkv.com/) to watch for and rip DVDs or BDs that you own automagically into their own directory.
It also looks up your discs title on IMDb to get the correct title before storing.

As an optional extra a converting script using [HandBrake](http://handbrake.fr/) has been included to compress movies to a reasonable size.

<hr>

#### Required for use

Python (Obviously)
* Created using 2.7.3 but should work with similar versions

MakeMKV
* http://makemkv.com/

IMDbPy
* sudo apt-get install python-imdbpy

### Optional

Handbrake - For converting and compressing
* http://handbrake.fr/
    1 sudo add-apt-repository ppa:stebbins/handbrake-releases
    2 sudo apt-get update && sudo apt-get install handbrake-cli