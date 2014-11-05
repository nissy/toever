toever
=======

About
-----
Evernote command line tool.

Install
-----

    $ sudo pip install toever

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

    $ curl http://wwwimages.adobe.com/www.adobe.com/content/dam/Adobe/en/legal/licenses-terms/pdf/Reader_11_0_jp.pdf | toever -f Adobe.pdf

Help
-----
    usage: toever [-h] [-t TITLE] [-f FILENAME] [--tags TAGS]
                     [--notebook NOTEBOOK] [-v]
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
      -v, --version         show program's version number and exit