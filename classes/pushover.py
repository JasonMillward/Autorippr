"""
Pushover Class


Released under the MIT license
Copyright (c) 2014, Jason Millward

@category   misc
@version    $Id: 1.7-test2, 2015-05-11 07:48:38 ACST $;
@author     Jason Millward
@license    http://opensource.org/licenses/MIT
"""
import logger
from chump import Application

class Pushover(object):

    def __init__(self, config):
        self.config = config

    def send_notification(self, notification_message):
        app = Application( self.config['app_key'] )
        user = app.get_user( self.config['user_key'] )
        message = user.send_message(notification_message)

        if message.is_sent:
            print "YAY"
