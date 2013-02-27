# coding: utf-8

from datetime import datetime, timedelta
import json
import web

import settings, model
from settings import base36decode

def internalerror(errstr=None):
    web.header('Content-type', 'application/json')
    if not errstr:
        errstr = 'Undefined'

    return web.internalerror(json.dumps(dict(error=errstr)))

class index:
    def GET(self, arg=None):
        # Init templator
        tpl = web.template.render(settings.TEMPLATE_DIR, base='base', globals={'_':_})

        # No argument, just return index
        if not arg:
            return tpl.index()

        phraseCode = base36decode(arg)

        # If an argument is provided then someone is trying to view a password
        try:
            phrase = model.get_phrase(
                code = phraseCode
            )
            seqID = phrase.get('id')
        except(model.ModelError), e:
            web.notfound()
            return tpl.notfound()

        # Update phrase counter
        try:
            model.update_phrase(seqID)
        except(), e:
            web.internalerror()
            raise

        # Get and calculate row data
        password = phrase.get('phrase')
        viewsleft = phrase.get('maxviews')-phrase.get('views')
        delta = datetime.now()-phrase.get('created')
        daysleft = phrase.get('maxdays')-delta.days

        # Calculate if maxviews or maxdays has been reached
        if daysleft <= 0 or viewsleft <= 0:
            try:
                deleted = model.delete_phrase(seqID)
            except:
                web.internalerror()
                raise

        return tpl.show(
            password=password,
            viewsleft=viewsleft,
            daysleft=daysleft
        )
