# -*- coding: utf-8 -*-

import re
import email
from email.header import decode_header
from email.utils import parsedate_tz, mktime_tz
import imaplib
import datetime
from logger import logger as log


class Gmail_checker(object):
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.imap_host = 'imap.gmail.com'
        self.email_default_encoding = 'iso-2022-jp'


    def _conv_date_format(self, date_string):
        """
        convert datetime format rfc2822 to iso8601
        and format year, month, day
        """
        time_tuple = parsedate_tz(date_string)
        time_stamp = mktime_tz(time_tuple)
        return datetime.date.fromtimestamp(time_stamp)


    def login(self):
        self.gmail = imaplib.IMAP4_SSL(self.imap_host)
        self.gmail.login(self.user, self.password)
        log.info('login')


    def logout(self):
        self.gmail.close()
        self.gmail.logout()
        log.info('logout')


    def mail_exists(self, subject_pattern):
        """
        Check the latest specified title email
        """
        self.gmail.select('inbox')
        self.gmail.select('Schoolbus')
        typ, data = self.gmail.search(None, '(ALL)')
        ids = data[0].split()
        log.info('ids={0}'.format(ids))
        for id in ids:
            typ, data = self.gmail.fetch(id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            _msg_subject = decode_header(msg.get('Subject'))[0][0]
            msg_encoding = decode_header(msg.get('Subject'))[0][1] or self.email_default_encoding
            msg_subject = _msg_subject.decode(msg_encoding)
            log.info(msg_subject)
            msg_date = self._conv_date_format(msg.get('Date'))
            log.info(msg_date)
            if msg_date == datetime.date.today():
                if re.match(subject_pattern, msg_subject):
                    self.remove_label(id)
                    return True
        else:
            return False


    def remove_label(self, id):
        self.gmail.store(id, '+FLAGS', '\\Deleted')
