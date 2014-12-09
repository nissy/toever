#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

application_name = 'toever'
version = '1.9.5'
user_filepath = os.environ['HOME'] + '/.' + application_name
sandbox = False
evernote_url = 'https://sandbox.evernote.com'
if sandbox:
    evernote_url = 'https://sandbox.evernote.com'
token_geturl = evernote_url + '/api/DeveloperToken.action'
