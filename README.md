Password Frank 
====

It's a password Pusher in python, web.py, bootstrap and jquery. 

Author
====

Stefan Midjich

License
====

CC0 - Creative Commons

Using
====

 1. Read and configure settings.py first, it's all about settings for directory names, database and locale. 
 2. Install web.py and psycopg2 as python libraries. 
 3. Install PostgreSQL database schema from tools directory. 
 4. Import wordlist into database.
 5. Deploy

To install the PostgreSQL schema you can simply paste it into psql. 

Importing of wordlist is done through REPL pretty easy, standing in the project root dir. 

    >>> from model import db
    >>> f = open('tools/wordlist.txt')
    >>> for line in f:
    ...  (freq, word) = line.split()
    ...  db.insert('wordlist', frequency=freq, word=word)

Either deploy using WSGI:

    WSGIPythonPath /var/www/frank
    WSGIScriptAlias / /var/www/frank/frank.py/
    AddType text/html .py
    Alias /static /var/www/frank/static
   
    <Directory /var/www/frank>
     AllowOverride None
     Order deny,allow
     allow from all
    </Directory>

Or just run from command line using:

    python frank.py

It's also advisable to use the tools/deletephrases.py in a crontab to delete old phrases that have reached their maxdays value regularly instead of waiting for page loads. 

In /etc/cron.d/passwordfrank for example, add this. 

    PATH=$PATH:/var/www/frank/tools
    0 0 * * * www-data  deletephrases.py

And use whatever user can access the file and the database. 

Translation
====

Only supports en\_US and sv\_SE out-of-box. To add more languages you need a Python 2.7 distribution with the msgfmt.py tool. 

This tool is usually installed on Linux already, only Mac OS users might have trouble finding it. 

 1. Edit i18n/messages.po if needed
 2. cp i18n/messages.po i18n/en\_US/LC\_MESSAGES/messages.po
 3. ./Python-2.7.1/Tools/i18n/msgfmt.py -o i18n/en\_US/LC\_MESSAGES/messages.mo i18n/sv\_SE/LC\_MESSAGES/messages.po

That's an example for english as main language, for any other language just edit the language specific i18n/sv\_SE/LC\_MESSAGES/messages.po and repeat step 3 for the language in question. 

Credit
====

Wordlist comes courtesy of somewhere on the internet, I don't know its origin. 

Hint
====

Add settings.py to .gitignore for easier pulls during deployment. 
