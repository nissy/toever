#!/usr/bin/env python
# -*- coding:utf-8 -*-

from evernote.api.client import EvernoteClient
from evernote.edam.type.ttypes import Note
from evernote.edam.type.ttypes import Resource, ResourceAttributes, Data
# from evernote.edam.error import ttypes as errors
from xml.sax.saxutils import escape
from clint import textui
import sys, os, argparse, mimetypes, hashlib, ConfigParser
from datetime import datetime
import config as sys_config


class ToEver():
    def __init__(self, token, sandbox=True):
        self.client = EvernoteClient(token=token, sandbox=sandbox)

    def createNote(self, title, content, tag=None, bookguid=None, resource=None):
        try:
            note_store = self.client.get_note_store()
            note = Note()
            if not tag is None:
                note.tagNames = tag
            if not bookguid is None:
                note.notebookGuid = bookguid
            if not resource is None:
                note.resources = [resource]
                content += "<span><en-media type=\"%s\" hash=\"%s\"/></span>" % (resource.mime, resource.data.bodyHash)
            note.title = title
            note.content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            note.content += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
            note.content += "<en-note>%s</en-note>" % content
            note_store.createNote(note)
            upload_limit_next_month = self.client.get_user_store().getUser().accounting.uploadLimitNextMonth
            user_upload = note_store.getSyncState().uploaded
            user_upload_state = "%s MB / %s MB" % (
                self.roundMbSize(user_upload), self.roundMbSize(upload_limit_next_month))
        except:
            print "\n" + user_upload_state + "\n" + textui.colored.red('Create note error')
            return 1
        print "\n" + user_upload_state + "\n" + textui.colored.blue("Created note title is '" + title + "'")
        return 0

    def listNotebooks(self):
        note_store = self.client.get_note_store()
        return note_store.listNotebooks()

    @staticmethod
    def getContentFormat(data):
        data = data.rstrip()
        data = '<div>' + escape(data) + '</div>'
        data = data.replace(' ', ' ')  # bytecode 20 -> c2a0
        data = data.replace('	', '    ')  # tab -> c2a0
        data = data.replace('<div></div>', '<div><br/></div>') + '\n'
        return data

    @staticmethod
    def isSetContent(data):
        return len(data.replace('<div><br/></div>', '')) != 0

    @staticmethod
    def roundMbSize(size):
        return str(round(size / (1024.0 ** 2)))


class UserConfig():
    def __init__(self, filepath):
        self.filepath = filepath
        self.user_config = ConfigParser.SafeConfigParser()
        try:
            self.user_config.read(self.filepath)
            self.getUserOption('developer_token')
        except:
            user_config = ConfigParser.RawConfigParser()
            user_config.add_section(sys_config.application_name)
            user_config.set(sys_config.application_name, 'developer_token')
            user_config.set(sys_config.application_name, 'notebook')
            user_config.set(sys_config.application_name, 'tags')
            with open(self.filepath, 'wb') as configfile:
                user_config.write(configfile)
                os.chmod(self.filepath, 0600)
            self.user_config.read(self.filepath)

    def getUserOption(self, option):
        return self.user_config.get(sys_config.application_name, option)

    def setDeveloperToken(self):
        print(textui.colored.green('Get Evernote developer token --> ' + sys_config.token_geturl))
        while True:
            developer_token = raw_input('Token: ')
            if self.isDeveloperToken(developer_token, sys_config.token_sandbox):
                self.user_config.set(sys_config.application_name, 'developer_token', developer_token)
                return self

    def setDefaultNotebook(self):
        print(textui.colored.green('Set ToEver default post notebook / Not enter if you do not set'))
        notebook = raw_input('Notebook: ')
        self.user_config.set(sys_config.application_name, 'notebook', notebook)
        return self

    def setDefaultTags(self):
        print(textui.colored.green('Set ToEver default post tags / Not enter if you do not set'))
        tags = raw_input('Tags: ')
        self.user_config.set(sys_config.application_name, 'tags', tags)
        return self

    def save(self):
        self.user_config.write(open(self.filepath, 'w'))

    @staticmethod
    def isDeveloperToken(token, sandbox=True):
        try:
            EvernoteClient(token=token, sandbox=sandbox).get_note_store()
        except:
            print(textui.colored.red('Token can not be used'))
            return False
        return True


class Util():
    @staticmethod
    def isBinary(data):
        for encoding in ['utf-8', 'shift-jis', 'euc-jp', 'iso2022-jp']:
            try:
                data = data.decode(encoding)
                break
            except:
                pass
        if isinstance(data, unicode):
            return False
        return True


def main():
    parser = argparse.ArgumentParser(description=sys_config.application_name + ' version ' + sys_config.version)
    parser.add_argument('file', nargs='?', action='store', help='file to send to evernote')
    parser.add_argument('-t', '--title', type=str, help='note title (omitted, the time is inputted automatically.)')
    parser.add_argument('-f', '--filename', type=str, help='note attachment file name')
    parser.add_argument('--tags', type=str, help='note tags (multiple tag separated by comma.)')
    parser.add_argument('--notebook', type=str, help='note notebook')
    parser.add_argument('--config', action='store_true', help='set user config')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + sys_config.version)

    args = parser.parse_args()
    user_config = UserConfig(sys_config.token_filepass)

    # Set user config
    if args.config:
        user_config.setDeveloperToken().setDefaultNotebook().setDefaultTags().save()
        return 0

    # File check
    if not args.file is None:
        if not os.path.isfile(args.file):
            print(textui.colored.red('File does not exist ' + args.file))
            return 1
        sys.stdin = open(args.file, 'r')
        if Util.isBinary(open(args.file, 'r').read()) and args.filename is None:
            args.filename = args.file

    # Get note title
    note_title = args.title
    if args.title is None:
        note_title = 'ToEver Post ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get note tags
    note_tags = None

    if args.tags is None and user_config.getUserOption('tags'):
        args.tags = user_config.getUserOption('tags')

    if not args.tags is None:
        note_tags = args.tags.split(',')

    # Get user developer token
    stdin_dafault = sys.stdin
    sys.stdin = open('/dev/tty', 'rt')

    if not user_config.isDeveloperToken(user_config.getUserOption('developer_token'), sys_config.token_sandbox):
        user_config.setDeveloperToken().save()

    sys.stdin = stdin_dafault

    toever = ToEver(user_config.getUserOption('developer_token'), sys_config.token_sandbox)

    # Set note bookguid
    note_bookguid = None

    if args.notebook is None and user_config.getUserOption('notebook'):
        args.notebook = user_config.getUserOption('notebook')

    if not args.notebook is None:
        for line in toever.listNotebooks():
            if line.name == args.notebook:
                note_bookguid = line.guid
                break

    # Set note content
    note_content = str()

    # Set binary stream
    if not args.filename is None:
        data = Data()
        data.body = sys.stdin.read()
        data.size = len(data.body)
        data.bodyHash = hashlib.md5(data.body).hexdigest()
        resource = Resource()
        resource.mime = mimetypes.guess_type(args.filename)[0]
        resource.data = data
        attr = ResourceAttributes()
        attr.fileName = args.filename
        resource.attributes = attr
        return toever.createNote(note_title, note_content, note_tags, note_bookguid, resource)

    # Set text stream
    try:
        for line in iter(sys.stdin.readline, ''):
            note_content += toever.getContentFormat(line)
            print(textui.colored.green(line.rstrip()))
    except:
        pass
    finally:
        # create note
        if toever.isSetContent(note_content):
            return toever.createNote(note_title, note_content, note_tags, note_bookguid)
    return 1


if __name__ == "__main__":
    sys.exit(main())
