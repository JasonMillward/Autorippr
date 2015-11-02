"""
Pushover Class


Released under the MIT license
Copyright (c) 2014, Jacob Carrigan

@category   misc
@version    $Id: 1.7-test2, 2015-05-11 07:48:38 ACST $;
@author     Jacob Carrigan
@license    http://opensource.org/licenses/MIT
"""

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib

class Smtp(object):

    def __init__(self, config):
        self.server = config['notification']['smtp_server']
        self.username = config['notification']['smtp_username']
        self.password = config['notification']['smtp_password']
        self.port = config['notification']['smtp_port']
        self.to_address = config['notification']['destination_email']
        self.from_address = config['notification']['source_email']

    def send_notification(self, notification_message):

        if self.from_address == 'username@gmail.com':
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
