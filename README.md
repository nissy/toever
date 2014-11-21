toever
=======
toEver is a command-line tool to create a note to Evernote.   

This command is specializing in the function to transmit a file and to make a note.  
The file of all the kinds can be transmitted.  
A binary file is registered as an attached file.   

A text and a binary file can be registered also from standard input.  
Standard input corresponds to the command which cannot be ended unless "tail -f" etc. send a signal.   

A tag, a notebook, and a title can be attached as an option, or a share link can be acquired.  


Install
-----
    $ sudo pip install toever

Setup
-----
[Please get the developer token of evernote](https://www.evernote.com/api/DeveloperToken.action)   
OSX have saved the token to keychain  

    $ toever --config

Usage
-----
File to send to evernote

    $ toever aaa.txt

    $ toever /etc/hosts -t 'My Hosts File'

    $ toever photo.jpg --notebook 'photo'
    
The note of evernote will be created if standard input is passed to toever.

    $ cat /etc/nginx/nginx.conf | toever --tags nginx,config --notebook linux

    $ toever -t 'localhost hosts file' < /etc/hosts
    
    $ tail -f /var/log/access_log | toever

If you specify a file name in the option, it is saved as an attachment.

    $ cat photo.jpg | toever -f photo.jpg

    $ curl https://www.python.org/static/img/python-logo.png | toever -f python.png --tags python

    $ wget -O - https://github.com/ngc224/toever/archive/master.tar.gz | toever -f master.tar.gz

It is possible to acquire a share URL If you add the "--share" option

    $ toever aaa.txt --share

    Created note title is 'ToEver Post 2014-11-20 21:19:16'
    Get note share url --> https://www.evernote.com/shard/s143/sh/5f55f19e-d5f4-4131-95e8-81f0b0...

Help
-----
    usage: toever [-h] [-t TITLE] [-f FILENAME] [--tags TAGS]
                  [--notebook NOTEBOOK] [--share] [--config] [-v]
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
      --share               get create note share url
      --config              set user config
      -v, --version         show program's version number and exit
