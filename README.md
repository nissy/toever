everstdin
=======

About
-----
Evernote command line tool.

Install
-----

    $ sudo pip install everstdin

Usage
-----

The note of evernote will be created if standard input is passed to everstdin.

    $ echo 'Note Content' | everstdin

    $ tail -f /var/log/access_log | everstdin -t 'apache access log'

    $ cat /etc/nginx/nginx.conf | everstdin --tags nginx,config --notebook linux

    $ everstdin -t 'localhost hosts file' < /etc/hosts

Help
-----

    usage: everstdin [-h] [-t TITLE] [--tags TAGS] [--notebook NOTEBOOK] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -t TITLE, --title TITLE
                            note title (omitted, the time is inputted
                            automatically.)
      --tags TAGS           note tags (multiple tag separated by comma.)
      --notebook NOTEBOOK   note notebook
      -v, --version         show program's version number and exit
