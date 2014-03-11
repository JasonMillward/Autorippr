"""Autorip

Usage:
  autorip.py --rip [options]
  autorip.py --compress [options]
  autorip.py --rip --compress [options]

Options:
  -h --help     Show this screen.
  --version     Show version.
  --debug       Output debug.
  --rip         Rip disc using makeMKV.
  --compress    Compress using handbrake.

"""
from docopt import docopt

__version__="1.5"

if __name__ == '__main__':
    arguments = docopt(__doc__, version=__version__)
    #print(arguments)

    if arguments['--rip']:
        print "Ripping!"

    if arguments['--compress']:
        print "Compressing"

