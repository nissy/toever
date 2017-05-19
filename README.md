toEver
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

Install mac osx
-----
    $ brew install nissy/toever/toever

Setup
-----
[Please get the developer token of evernote](https://www.evernote.com/api/DeveloperToken.action)   
OSX have saved the token to keychain  

    $ toever --config

Usage
-----
File to send to evernote

    $ toever aaa.txt

    $ toever aaa.txt bbb.jpg ccc.zip

    $ toever photo1.jpg photo2.jpg --notebook 'photo'
    
The note of evernote will be created if standard input is passed to toever.

    $ cat /etc/nginx/nginx.conf | toever --tags nginx,config --notebook linux

    $ toever -t 'localhost hosts file' < /etc/hosts
    
    $ tail -f /var/log/access_log | toever

If you specify a file name in the option, it is saved as an attachment.
 
    $ tar cvz /etc/nginx | toever -f nginx.tar.gz

    $ curl https://www.python.org/static/img/python-logo.png | toever -f python.png

    $ wget -O - https://github.com/nissy/toever/archive/master.tar.gz | toever -f master.tar.gz

It is possible to acquire a share URL If you add the "--share" option

    $ toever ~/.ssh/authorized_keys --share
    ...
    Created note title is 'toEver Post 2014-11-20 21:19:16' [50.0 MB / 4096.0 MB]
    share link --> https://www.evernote.com/shard/s143/sh/5f55f19e-d5f4-4131-95e8-81f0b0...

Help
-----
    usage: toever [-h] [-f FILENAME] [-t TITLE] [--tags TAGS]
                     [--notebook NOTEBOOK] [--config] [--hide] [--share] [-v]
                     [file [file ...]]
    
    positional arguments:
      file                  file to send to evernote
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FILENAME, --filename FILENAME
                            set note attachment file name (When the name is
                            designated, it processed as attachment file.)
      -t TITLE, --title TITLE
                            set note title (omitted, the time is inputted
                            automatically.)
      --tags TAGS           set note tags (multiple tag separated by comma.)
      --notebook NOTEBOOK   set note notebook
      --config              set user config
      --hide                hide the display message (except share link)
      --share               set note share link
      -v, --version         show program's version number and exit
