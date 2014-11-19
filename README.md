toever
=======

About
-----
Evernote command line tool.

Install
-----
    $ sudo pip install toever

Setup
-----
OSX have saved the token to keychain

    $ toever --config

Usage
-----
File to send to evernote

    $ toever ~/aaa.txt

    $ toever /etc/hosts -t 'My Hosts File'

    $ toever ~/photo.jpg --notebook 'photo'
    
The note of evernote will be created if standard input is passed to toever.

    $ cat /etc/nginx/nginx.conf | toever --tags nginx,config --notebook linux

    $ toever -t 'localhost hosts file' < /etc/hosts
    
    $ tail -f /var/log/access_log | toever

If you specify a file name in the option, it is saved as an attachment.

    $ cat ~/photo.jpg | toever -f photo.jpg

    $ curl https://www.python.org/static/img/python-logo.png | toever -f python.png --tags python

    $ wget -O - https://github.com/ngc224/toever/archive/master.tar.gz | toever -f master.tar.gz

Help
-----
    usage: toever [-h] [-t TITLE] [-f FILENAME] [--tags TAGS]
                     [--notebook NOTEBOOK] [--config] [-v]
                     [file]
    
    positional arguments:
      file                  file to send to evernote
    
    optional arguments:
      -h, --help            show this help message and exit
      -t TITLE, --title TITLE
                            note title (omitted, the time is inputted
                            automatically.)
      -f FILENAME, --filename FILENAME
                            note attachment file name
      --tags TAGS           note tags (multiple tag separated by comma.)
      --notebook NOTEBOOK   note notebook
      --config              set user config
      -v, --version         show program's version number and exit
