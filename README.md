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

If you specify a file name in the option, it is saved as an attachment.

    $ cat ~/Desktop/aaa.jpg | everstdin -t aaa --filename aaa.jpg

    $ < ~/Desktop/bbb.jpg everstdin --filename bbb.jpg

    $ curl http://www.python.jp/images/pyjug.png | everstdin --filename python.png --tags python

Help
-----

    usage: everstdin [-h] [-t TITLE] [-f FILENAME] [--tags TAGS]
                        [--notebook NOTEBOOK] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -t TITLE, --title TITLE
                            note title (omitted, the time is inputted
                            automatically.)
      -f FILENAME, --filename FILENAME
                            note attachment file name
      --tags TAGS           note tags (multiple tag separated by comma.)
      --notebook NOTEBOOK   note notebook
      -v, --version         show program's version number and exit