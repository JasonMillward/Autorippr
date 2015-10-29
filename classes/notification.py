"""
Notification Class


Released under the MIT license
Copyright (c) 2014, Ian Bird

@category   misc
@version    $Id: 1.7-test2, 2015-05-11 07:48:38 ACST $;
@author     Jacob Carrigan
@license    http://opensource.org/licenses/MIT
"""

import os
import subprocess
import logger

class Notification(object):

    def __init__(self, config, debug, silent):
        self.log = logger.Logger("Notification", debug, silent)
        self.server = config['smtp_server']
        self.username = config['smtp_username']
        self.password = config['smtp_password']
        self.port = config['smtp_port']
        self.to_address = config['destination_email']
        self.from_email = config['source_email']
        
    def _send(self, status):
        import smtplib
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText
        
        if self.source_email == 'username@gmail.com':
            self.logging.error('Email address has not been set correctly, ignoring send request from: %s' % self.from_address)
            return
        
        msg = MIMEMultipart()
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = "Autorippr"
        
        body = status
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(self.server, self.port)
        server.starttls()
        server.login(self.from_address, self.password)
        text = msg.as_string()
        server.sendmail(self.from_address, self.to_address, text)
        server.quit()

    def rip_complete(self,dbvideo):
        
        status = 'Rip of %s complete' % dbvideo.vidtitle
        self._send(status)

    def compress_complete(self,dbvideo):
        
        status = 'Compress of %s complete' % dbvideo.vidtitle
        self._send(status)
        
    def extra_complete(self,tracks,dbvideo):
        
        status = 'Extra of %s complete' % dbvideo.vidtitle
        self._send(status)
