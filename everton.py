#!/usr/bin/env python
# -*- coding:utf-8 -*-

from evernote.api.client import EvernoteClient
from evernote.edam.type.ttypes import Note
#from evernote.edam.error import ttypes as Errors
from xml.sax.saxutils import escape
import sys, signal, os, getpass
import config


class Everton():

    def __init__(self, token, note_title):
        self.client = EvernoteClient(token=token)
        self.note_title = note_title
        self.note_content = str()

    def setNote(self):
        def handler(signum, frame):
            def inHandler(signum, frame):
                sys.exit(0)
            signal.signal(signal.SIGINT, inHandler)
            if self.isSetContent(self.note_content):
                self.makeNote()
            sys.exit(0)

        signal.signal(signal.SIGINT, handler)

        for line in iter(sys.stdin.readline, ''):
            self.note_content += self.getContentFormat(line)
            print line.replace('\r\n', '').replace('\r', '').replace('\n', '')
        if self.isSetContent(self.note_content):
            self.makeNote()

    def makeNote(self):
        note_store = self.client.get_note_store()
        note = Note()
        note.title = self.note_title
        note.content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        note.content += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
        note.content += "<en-note>%s</en-note>" % self.note_content

        try:
            note_store.createNote(note)
        except:
            return False
        print "Created note title is '" + self.note_title + "'"

        return True

    @staticmethod
    def getContentFormat(data):
        data = data.replace('\r\n', '').replace('\n', '')
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
        print 'Get Evernote developer token -> ' + config.token_geturl
        token = getpass.getpass(prompt='Set Token: ')
        f = open(filepass, 'w')
        f.write(token)
        f.close()
        os.chmod(filepass, 0600)
        return token

    def isDeveloperToken(self, token):
        try:
            EvernoteClient(token=token).get_note_store()
        except:
            return False
        return True


def main():

    auth = Auth()

    # Get user developer token
    stdin_dafault = sys.stdin
    sys.stdin = file('/dev/tty')

    developer_token = auth.getDeveloperToken(config.token_filepass)

    while True:
        if auth.isDeveloperToken(developer_token):
            break
        developer_token = auth.setDeveloperToken(config.token_filepass)

    sys.stdin = stdin_dafault

    # Get note title
    note_title = config.note_title_default
    if len(sys.argv) > 1:
        note_title = sys.argv[1]

    # Set note content
    everton = Everton(developer_token, note_title)
    everton.setNote()

if __name__ == "__main__":
    main()
