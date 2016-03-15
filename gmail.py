# -*- coding: utf-8 -*-

import re
import email
from email.header import decode_header
from email.utils import parsedate_tz, mktime_tz
import imaplib
import datetime


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


    def _time_stamp(self):
        return "{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())


    def login(self):
        self.gmail = imaplib.IMAP4_SSL(self.imap_host)
        self.gmail.login(self.user, self.password)
        print('login:{0}'.format(self._time_stamp()))


    def logout(self):
        self.gmail.close()
        self.gmail.logout()
        print('logout:{0}'.format(self._time_stamp()))


    def mail_exists(self, subject_pattern):
        """
        Checck the latest unread specified title email
        """
        self.gmail.select('inbox')
        self.gmail.select('Schoolbus')
        typ, data = self.gmail.search(None, '(ALL)')
        ids = data[0].split()
        print('ids={0} {1}'.format(ids, self._time_stamp()))
        for id in ids:
            typ, data = self.gmail.fetch(id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            _msg_subject = decode_header(msg.get('Subject'))[0][0]
            msg_encoding = decode_header(msg.get('Subject'))[0][1] or self.email_default_encoding
            msg_subject = _msg_subject.decode(msg_encoding)
            print(msg_subject)
            msg_date = self._conv_date_format(msg.get('Date'))
            print(msg_date)
            if msg_date == datetime.date.today():
                if re.match(subject_pattern, msg_subject):
                    self.gmail.store(id, '+FLAGS', '\\Deleted')
                    return True
        else:
            return False


    def remove_label(self, id, label):
        self.gmail.store(id, '-X-GM-LABELS', label)
