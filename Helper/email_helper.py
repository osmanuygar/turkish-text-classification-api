# -*- coding: utf-8 -*-
# ! /usr/local/bin/python
import traceback
import logging
import sys
import os
import re
# from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import SMTP  # use this for standard SMTP protocol   (port 25, no encryption)
from email.mime.text import MIMEText


class mailHelper:
    def __init__(self, sender, username, password, smtpServer, port=587, textContentType='html'):
        self.sender = sender
        self.smtpServer = smtpServer
        self.port = port
        self.username = username
        self.password = password
        self.textContentType = textContentType

    def sendMail(self, sourceMail, toarrMail, subject, content):
        try:
            print
            self.smtpServer, self.port
            self.conn = SMTP(self.smtpServer, self.port)

            # noreply doe not need
            # conn.connect()
            # conn.login(USERNAME, PASSWORD)

            self.conn.set_debuglevel(False)

            msg = MIMEText(content, self.textContentType)
            msg['Subject'] = subject
            msg['From'] = sourceMail  # some SMTP servers will do this automatically, not all
            msg['To'] = ';'.join(toarrMail)  # some SMTP servers will do this automatically, not all

            try:
                self.conn.sendmail(self.sender, toarrMail, msg.as_string())
            finally:
                self.conn.close()

        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            tb = traceback.format_exc()
            print
            tb
            logging.error(
                'Sending mail failed with:' + str(exc_type) + ' ' + fname + ' ' + str(exc_tb.tb_lineno) + '\n' + tb)
            start = False