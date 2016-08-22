# -*- coding: utf-8 -*-
"""
SMTP Class


Released under the MIT license
Copyright (c) 2014, Jacob Carrigan

@category   misc
@version    $Id: 1.7-test4, 2015-11-09 12:30:44 ACDT $;
@author     Jacob Carrigan
@license    http://opensource.org/licenses/MIT
"""

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import logger


class Smtp(object):

    def __init__(self, config, debug, silent):
        self.server = config['smtp_server']
        self.username = config['smtp_username']
        self.password = config['smtp_password']
        self.port = config['smtp_port']
        self.to_address = config['destination_email']
        self.from_address = config['source_email']
        self.log = logger.Logger("SMTP", debug, silent)

    def send_notification(self, notification_message):

        if self.from_address == 'username@gmail.com':
            self.logging.error(
                'Email address has not been set correctly, ignoring send request from: {}'.format(self.from_address))
            return

        msg = MIMEMultipart()
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = "Autorippr"

        msg.attach(MIMEText(notification_message, 'plain'))

        server = smtplib.SMTP(self.server, self.port)
        server.starttls()
        server.login(self.from_address, self.password)

        text = msg.as_string()
        server.sendmail(self.from_address, self.to_address, text)
        server.quit()
