"""
Basic analytics

The purpose of this file is to simply send a 'ping' with a unique identifier
and the script version once a day to give an indication of unique users

This has been added because Github doesn't show a download counter, I have no
way of knowing if this script is even being used (except for people telling me
it broke).

You are free to opt-out by disabling the config option

    analytics:
        enable:     True <- make this False

If the computer doesn't have internet access the script will continue as normal


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.7-test4, 2015-11-09 12:30:44 ACDT $;
@author     Jason Millward
@license    http://opensource.org/licenses/MIT
"""


def ping(version):
    """
        Send a simple ping to my server
            to see how many people are using this script
    """
    try:
        import uuid
        import requests
        import json
        import os
        import time

        data = {
            "uuid": uuid.getnode(),
            "version": version
        }

        datefile = "/tmp/%s" % time.strftime("%Y%m%d")

        if not os.path.isfile(datefile):

            with open(datefile, 'w'):
                os.utime(datefile, None)

            requests.post(
                'http://api.jcode.me/autorippr/stats',
                data=json.dumps(data),
                timeout=5
            )

    except:
        pass
