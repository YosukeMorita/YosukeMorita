# -*- coding: utf-8 -*-

import time
from twilio.rest import TwilioRestClient
from twilio import TwilioRestException
from gmail import Gmail_checker
from setting import SID, SECRET, TARGET, FROM, ID, PASS, URL


def makecall(sid, secret, target, from_, url, timeout=10):
    try:
        client = TwilioRestClient(sid, secret)
        call = client.calls.create(
                to=target,
                from_=from_,
                url=url,
                timeout=timeout
                )

        print(call.sid)

    except TwilioRestException as e:
        print(e)

if __name__ == '__main__':
    try:
        gmail = Gmail_checker(ID, PASS)
        while True:
            if gmail.mail_exists(u'まもなく'):
                makecall(SID, SECRET, TARGET, FROM, URL)
            time.sleep(15)
    except KeyboardInterrupt:
        print('\nbreak')
