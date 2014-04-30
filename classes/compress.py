
def compress(config):
    """
        Main function for compressing
        Does everything
        Returns nothing
    """
    log = logger.logger("Compress", config['debug'])

    hb = handbrake.handBrake(config['debug'])

    log.debug("Compressing started successfully")
    log.debug("Looking for movies to compress")

    if hb.loadMovie():
        log.info( "Compressing %s" % hb.getMovieTitle())

        with stopwatch.stopwatch() as t:
            convert = hb.convert(
                args=config['com'],
                nice=int(config['nice'])
            )

        if convert:
            log.info("Movie was compressed and encoded successfully")

            log.info( ("It took %s minutes to compress %s" %
                    (t.minutes, hb.getMovieTitle()))
            )
        else:
            log.info( "HandBrake did not complete successfully")

    else:
        log.info( "Queue does not exist or is empty")

