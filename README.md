everton
=======

About
-----
Evernote command line tool.

Install
-----

    $ pip install everton

Usage
-----

Standard input is sent to Evernote.

    $ echo 'Note Content' | everton 'Note Title'

    $ tail -f /var/log/access_log | everton 'apache access log' --tags accesslog

    $ cat /etc/nginx/nginx.conf | everton 'nginx conf' --tags nginx,config

    $ everton 'localhost hosts file' < /etc/hosts

Help
-----
    $ everton -h

    usage: everton [-h] [--tags TAGS] [--notebook NOTEBOOK] [--version] title
    
    everton version 0.4
    
    positional arguments:
      title                note title
    
    optional arguments:
      -h, --help           show this help message and exit
      --tags TAGS          note tags (multiple tag separated by comma)
      --notebook NOTEBOOK  note notebook
      --version            show program's version number and exit
