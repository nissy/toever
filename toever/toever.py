#!/usr/bin/env python
# -*- coding:utf-8 -*-

from evernote.api.client import EvernoteClient
from evernote.edam.type.ttypes import Note
from evernote.edam.type.ttypes import Resource, ResourceAttributes, Data
# from evernote.edam.error import ttypes as errors
from xml.sax.saxutils import escape
from datetime import datetime
from clint import textui
import sys, os, argparse, mimetypes, hashlib, ConfigParser
import keyring
import chardet
import config as sys_config


class ToEver():
    def __init__(self, token, sandbox=True):
        self.client = EvernoteClient(token=token, sandbox=sandbox)
        self.token = token
        self.hide = False
        self.share = False
        self.tag = None
        self.bookguid = None

    def createNote(self, title, content, resource=None):
        user_store = self.client.get_user_store()
        note_store = self.client.get_note_store()
        try:
            note = Note()
            note.tagNames = self.tag
            note.notebookGuid = self.bookguid
            if resource is not None:
                note.resources = [resource]
                content += "<span><en-media type=\"%s\" hash=\"%s\"/></span>" % (resource.mime, resource.data.bodyHash)
            note.title = title
            note.content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            note.content += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
            note.content += "<en-note>%s</en-note>" % content
            created_note = note_store.createNote(note)
        except:
            return textui.colored.red('Create note error')

        note_share_url = None
        note_share_resource_url = None
        if self.share:
            note_share_url = ToEver.getNoteShareUrl(
                sys_config.evernote_url,
                user_store.getUser().shardId,
                created_note.guid,
                note_store.shareNote(self.token, created_note.guid)
            )
            if resource is not None:
                for x in created_note.resources:
                    note_share_resource_url = note_share_url + "/res/%s/%s" % (x.guid, x.attributes.fileName)

        if not self.hide:
            message = "\n" + "Created note title is '" + title + "'"
            message += " [" + ToEver.getUserUploadState(note_store.getSyncState().uploaded, user_store.getUser().accounting.uploadLimitNextMonth) + "]"
            if note_share_url is not None:
                message += "\n" + "Share URL --> " + note_share_url
                if note_share_resource_url is not None:
                    message += "\n" + "Share attachment URL --> " + note_share_resource_url
            print(textui.colored.blue(message))
        elif note_share_url is not None:
            print(textui.colored.blue(note_share_url))
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
    def getNoteShareUrl(url, shard_id, note_guid, share_key):
        return "%s/shard/%s/sh/%s/%s" % (url, shard_id, note_guid, share_key)

    @staticmethod
    def getRoundMbSize(size):
        return str(round(size / (1024.0 ** 2)))

    @staticmethod
    def getUserUploadState(user_upload, upload_limit_next_month):
        return "%s MB / %s MB" % (ToEver.getRoundMbSize(user_upload), ToEver.getRoundMbSize(upload_limit_next_month))


class UserConfig():
    def __init__(self, filepath):
        self.filepath = filepath
        self.user_config = ConfigParser.SafeConfigParser()
        try:
            if not os.path.isfile(self.filepath):
                raise IOError(self.filepath)
        except:
            user_config = ConfigParser.RawConfigParser()
            user_config.add_section(sys_config.application_name)
            user_config.set(sys_config.application_name, 'notebook', '')
            user_config.set(sys_config.application_name, 'tags', '')
            with open(self.filepath, 'wb') as configfile:
                user_config.write(configfile)
                os.chmod(self.filepath, 0644)
        self.user_config.read(self.filepath)

    def getUserOption(self, option):
        if self.user_config.has_option(sys_config.application_name, option):
            return self.user_config.get(sys_config.application_name, option)

    def setDeveloperToken(self):
        print(textui.colored.green('Get Evernote DeveloperToken URL --> ' + sys_config.token_geturl))
        while True:
            developer_token = raw_input('Token: ')
            if self.isDeveloperToken(developer_token, sys_config.sandbox):
                keyring.set_password(sys_config.application_name, 'developer_token', developer_token)
                return self

    def setDefaultNotebook(self):
        print(textui.colored.green('Set toEver default post notebook / Not enter if you do not set'))
        notebook = raw_input('Notebook: ')
        self.user_config.set(sys_config.application_name, 'notebook', notebook)
        return self

    def setDefaultTags(self):
        print(textui.colored.green('Set toEver default post tags / Not enter if you do not set'))
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
        return chardet.detect(data)['encoding'] is None


def main():
    parser = argparse.ArgumentParser(description=sys_config.application_name + ' version ' + sys_config.version)
    parser.add_argument('file', nargs='?', action='store', help='file to send to evernote')
    parser.add_argument('-t', '--title', type=str, help='note title (omitted, the time is inputted automatically.)')
    parser.add_argument('-f', '--filename', type=str, help='note attachment file name')
    parser.add_argument('--tags', type=str, help='note tags (multiple tag separated by comma.)')
    parser.add_argument('--notebook', type=str, help='note notebook')
    parser.add_argument('--share', action='store_true', help='get note share url')
    parser.add_argument('--hide', action='store_true', help='hide the display')
    parser.add_argument('--config', action='store_true', help='set user config')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + sys_config.version)

    args = parser.parse_args()
    user_config = UserConfig(sys_config.user_filepath)

    # Set user config
    if args.config:
        try:
            user_config.setDeveloperToken().setDefaultNotebook().setDefaultTags().save()
        except:
            return 1
        return 0

    # File check
    if args.file is not None:
        if not os.path.isfile(args.file):
            return textui.colored.red('File does not exist ' + args.file)
        sys.stdin = open(args.file, 'r')
        if Util.isBinary(open(args.file, 'r').read()) and args.filename is None:
            args.filename = os.path.basename(args.file)

    # Get user developer token
    stdin_dafault = sys.stdin
    sys.stdin = open('/dev/tty', 'rt')
    if not user_config.isDeveloperToken(keyring.get_password(sys_config.application_name, 'developer_token'), sys_config.sandbox):
        user_config.setDeveloperToken()
    sys.stdin = stdin_dafault

    toever = ToEver(keyring.get_password(sys_config.application_name, 'developer_token'), sys_config.sandbox)

    # Get note title
    if args.title is None:
        args.title = 'toEver Post ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get note tags
    if args.tags is None and user_config.getUserOption('tags'):
        args.tags = user_config.getUserOption('tags')
    if args.tags is not None:
        toever.tag = args.tags.split(',')

    # Set note bookguid
    if args.notebook is None and user_config.getUserOption('notebook'):
        args.notebook = user_config.getUserOption('notebook')
    if args.notebook is not None:
        for line in toever.listNotebooks():
            if line.name == args.notebook:
                toever.bookguid = line.guid
                break

    # Set note tags share
    toever.hide = args.hide
    toever.share = args.share

    # Set note content
    note_content = str()

    # Set binary stream
    if args.filename is not None:
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
        if not args.hide:
            print(textui.colored.green("Attachment file is '" + attr.fileName + "'"))
        return toever.createNote(args.title, note_content, resource)

    # Set text stream
    try:
        for line in iter(sys.stdin.readline, ''):
            note_content += toever.getContentFormat(line)
            if not args.hide:
                print(textui.colored.green(line.rstrip()))
    except:
        pass
    finally:
        # create note
        if toever.isSetContent(note_content):
            return toever.createNote(args.title, note_content)
    return textui.colored.red('Create note error')


if __name__ == "__main__":
    sys.exit(main())
