#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

application_name = 'toever'
version = '1.9.3'

user_filepath = os.environ['HOME'] + '/.' + application_name
tmp_filepath = '/tmp/toever'
sandbox = False
evernote_url = 'https://www.evernote.com'
token_geturl = 'https://www.evernote.com/api/DeveloperToken.action'

if sandbox:
    evernote_url = 'https://sandbox.evernote.com'
    token_geturl = 'https://sandbox.evernote.com/api/DeveloperToken.action'
