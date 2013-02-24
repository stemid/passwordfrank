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

Read through settings.py first, the beginning of that file is all about settings for directory names, database and locale. 

Install PostgreSQL database schema from tools directory. 

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

Translation
====

Only supports en\_US and sv\_SE out-of-box. To add more languages you need a Python 2.7 distribution with the msgfmt.py tool. 

This tool is usually installed on Linux already, only Mac OS users might have trouble finding it. 

 1. Edit i18n/messages.po if needed
 2. cp i18n/messages.po i18n/en\_US/LC\_MESSAGES/messages.po
 3. ./Python-2.7.1/Tools/i18n/msgfmt.py -o i18n/en\_US/LC\_MESSAGES/messages.mo i18n/sv\_SE/LC\_MESSAGES/messages.po

That's an example for english as main language, for any other language just edit the language specific i18n/sv\_SE/LC\_MESSAGES/messages.po and repeat step 3 for the language in question. 
