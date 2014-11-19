#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

application_name = 'toever'
version = '1.7.0'

user_filepath = os.environ['HOME'] + '/.' + application_name
token_sandbox = False
token_geturl = 'https://www.evernote.com/api/DeveloperToken.action'

if token_sandbox:
    token_geturl = 'https://sandbox.evernote.com/api/DeveloperToken.action'
