#!/usr/bin/env python
# Script to delete phrases from database by date using 
# crontab. Instead of waiting around for page loads. 
# Must run in crontab from its current directory, 
# tools/, to find the modules from project root. 

from os import path
from sys import exit, stderr, path as pythonpath
from datetime import datetime, timedelta

# Import db model from PROJECT_ROOT
parentdir = path.dirname(path.dirname(path.abspath(__file__)))
pythonpath.insert(0,parentdir)
import model
from model import db

# Delete any old phrases starting from right now. 
now = datetime.now()

try:
    rows = db.select('stash', order='id asc')
except:
    raise

for row in rows:
    maxdays = row.get('maxdays')
    created = row.get('created')
    seqID = row.get('id')

    delta = now-created

    if maxdays > delta.days:
        continue
    else:
        try:
            model.delete_phrase(seqID)
        except:
            raise
        else:
            print >> stderr, "Deleted phrase ID: %d" % seqID

exit(0)
