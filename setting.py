## -*- coding: utf-8 -*-

import os
import configparser

config_file = '~/.email2phone'
config = configparser.ConfigParser()
try:
    config.read(os.path.expanduser(config_file))
    e2p_conf = dict(config.items('email2phone'))
    SID = e2p_conf['sid']
    SECRET = e2p_conf['secret']
    TARGET = e2p_conf['target']
    FROM = e2p_conf['from']
    URL = e2p_conf['url']
    ID = e2p_conf['id']
    PASS = e2p_conf['pass']
except Exception as e:
    print(e)
