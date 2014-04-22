#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

application_name = 'everstdin'
version = '1.0'

token_sandbox = False
token_filepass = os.environ['HOME'] + '/.' + application_name
token_geturl = 'https://www.evernote.com/api/DeveloperToken.action'

if token_sandbox:
    token_geturl = 'https://sandbox.evernote.com/api/DeveloperToken.action'
