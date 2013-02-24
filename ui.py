# coding: utf-8

from datetime import datetime, timedelta
import json
import web

import settings, model
from settings import base36decode

def internalerror(errstr):
    web.header('Content-type', 'application/json')

    return web.internalerror(json.dumps(dict(error=errstr)))

class index:
    def GET(self, arg=None):
        # Init templator
        tpl = web.template.render(settings.TEMPLATE_DIR, base='base', globals={'_':_})

        # No argument, just return index
        if not arg:
            return tpl.index()

        seqID = base36decode(arg)

        # If an argument is provided then someone is trying to view a password
        try:
            row = model.get_phrase(seqID)
        except(model.ModelError), e:
            web.notfound()
            return tpl.notfound()

        try:
            model.update_phrase(seqID)
        except(), e:
            web.internalerror()
            raise

        password = row.get('phrase')
        viewsleft = row.get('maxviews')-row.get('views')
        delta = datetime.now()-row.get('created')
        daysleft = delta.days

        # Calculate if maxviews or maxdays has been reached
        if delta.seconds <= 0 or viewsleft <= 0:
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
