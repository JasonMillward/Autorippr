import os
import ConfigParser
from handbrake import HandBrake
from timer import Timer
from tendo import singleton

me = singleton.SingleInstance()
DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = "%s/../settings.cfg" % DIR

def read_value(key):
    """
    read_value temp docstring
    """
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)
    to_return = config.get('HANDBRAKE', key)
    config = None
    return to_return


def compress():
    """
    compress temp docstring
    """

    log = Logger("compress", read_value('debug'))

    hb_nice = int(read_value('nice'))
    hb_cli = read_value('com')
    hb_out = read_value('temp_output')

    hb_api = HandBrake(
        read_value('debug')
    )

    if hb_api.loadMovie():
        log.info( "Encoding and compressing %s" % hb_api.getMovieTitle()
        stopwatch = Timer()

        if hb_api.convert(args=hb_cli, nice=hb_nice, output=hb_out):
            log.info( "Movie was compressed and encoded successfully")

            stopwatch.stop()
            log.info( ("It took %s minutes to compress %s"
                %
                (stopwatch.getTime(), hb_api.getMovieTitle())))
        else:
            stopwatch.stop()
            log.info( "HandBrake did not complete successfully")
    else:
        log.info( "Queue does not exist or is empty")


if __name__ == '__main__':
    compress()
