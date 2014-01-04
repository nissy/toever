#!/usr/bin/env python
# -*- coding:utf-8 -*-

from evernote.api.client import EvernoteClient
from evernote.edam.type.ttypes import Note
#from evernote.edam.error import ttypes as errors
from xml.sax.saxutils import escape
from clint import textui
import sys, os, getpass, argparse
import config


class Everton():

    def __init__(self, token, sandbox=True):
        self.client = EvernoteClient(token=token, sandbox=sandbox)

    def createNote(self, title, content, tag=None, bookguid=None):
        try:
            note_store = self.client.get_note_store()
            note = Note()
            if not tag is None:
                note.tagNames = tag
            if not bookguid is None:
                note.notebookGuid = bookguid
            note.title = title
            note.content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            note.content += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
            note.content += "<en-note>%s</en-note>" % content
            note_store.createNote(note)
        except:
            return False
        return True


    def listNotebooks(self):
        note_store = self.client.get_note_store()
        return note_store.listNotebooks()

    @staticmethod
    def getContentFormat(data):
        data = data.rstrip()
        data = '<div>' + escape(data) + '</div>'
        data = data.replace('<div></div>', '<div><br/></div>')
        return data

    @staticmethod
    def isSetContent(data):
        return len(data.replace('<div><br/></div>', '')) != 0


class Auth():

    def getDeveloperToken(self, filepass):
        if os.path.exists(filepass):
            f = open(filepass, 'r')
            token = f.readline()
            f.close()
            return token
        return self.setDeveloperToken(filepass)

    def setDeveloperToken(self, filepass):
        print('Get Evernote developer token -> ' + config.token_geturl)
        token = getpass.getpass(prompt='Input token: ')
        f = open(filepass, 'w')
        f.write(token)
        f.close()
        os.chmod(filepass, 0600)
        return token

    def isDeveloperToken(self, token, sandbox=True):
        try:
            EvernoteClient(token=token, sandbox=sandbox).get_note_store()
        except:
            return False
        return True


def main():

    parser = argparse.ArgumentParser(description='everton version 0.3')
    parser.add_argument('title', type=str, help='note title')
    parser.add_argument('--tags', type=str, help='note tags (multiple tag separated by comma)')
    parser.add_argument('--notebook', type=str, help='note notebook')
    parser.add_argument('--version', action='version', version='%(prog)s 0.3')
    args = parser.parse_args()

    # Get note title
    note_title = args.title

    # Get note tags
    note_tags = None
    if not args.tags is None:
        note_tags = args.tags.split(',')

    # Get user developer token
    auth = Auth()
    stdin_dafault = sys.stdin
    sys.stdin = open('/dev/tty', 'rt')

    try:
        while True:
            developer_token = auth.getDeveloperToken(config.token_filepass)
            if auth.isDeveloperToken(developer_token, config.token_sandbox):
                break
            developer_token = auth.setDeveloperToken(config.token_filepass)
    except:
        sys.exit(0)

    sys.stdin = stdin_dafault

    everton = Everton(developer_token, config.token_sandbox)

    # Set note bookguid
    note_bookguid = None
    if not args.notebook is None:
        for line in everton.listNotebooks():
            if line.name == args.notebook:
                note_bookguid = line.guid
                break

    # Set note content
    note_content = str()

    try:
        for line in iter(sys.stdin.readline, ''):
            note_content += everton.getContentFormat(line)
            print(textui.colored.green(line.rstrip()))
    except:
        pass
    finally:
        # create note
        if everton.isSetContent(note_content):
            result = everton.createNote(note_title, note_content, note_tags, note_bookguid)
            if result:
                print("\n" + textui.colored.blue("Created note title is '" + note_title + "'"))
            else:
                print("\n" + textui.colored.red('Create note error'))

if __name__ == "__main__":
    main()
