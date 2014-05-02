"""
Basic analtics

The purpose of this file is to simply send a 'ping' with a unique identifier
to give an indication of unique users

Because Github doesn't show a download counter, I have no way of knowing if
this script is even being used (except for people telling me it broke).

You are free to opt-out by disabling the config option

    analytics:
        enable:     True <- make this False

If the computer doesn't have internet access the script will continue as normal


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""

def ping():
    """
        Send a simple

    """
    try:
        import uuid
        import requests
        import json

        data = {
            "uuid": uuid.getnode()
        }

        requests.post(
            'http://api.jcode.me/autoripper/stats',
            data=json.dumps(data),
            timeout=5
        )

    except :
        pass

