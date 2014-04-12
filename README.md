everstdin
=======

About
-----
Evernote command line tool.

Install
-----

    $ pip install everstdin

Usage
-----

Standard input is sent to Evernote.

    $ echo 'Note Content' | everstdin -t 'Note Title'

    $ tail -f /var/log/access_log | everstdin 'apache access log' --tags accesslog

    $ cat /etc/nginx/nginx.conf | everstdin --tags nginx,config --notebook linux

    $ everstdin 'localhost hosts file' < /etc/hosts

Help
-----
    $ everstdin -h
    usage: everstdin.py [-h] [-t TITLE] [--tags TAGS] [--notebook NOTEBOOK] [-v]

    everstdin version 0.6

    optional arguments:
      -h, --help            show this help message and exit
      -t TITLE, --title TITLE
                            note title (omitted, the time is inputted
                            automatically.)
      --tags TAGS           note tags (multiple tag separated by comma.)
      --notebook NOTEBOOK   note notebook
      -v, --version         show program's version number and exit
