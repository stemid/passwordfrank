from datetime import datetime, timedelta
from uuid import uuid4
import json
import web

import settings, model
from settings import generate_password, base36encode, base36decode

# Helper function for formatting datetime objects to json
def dateHandler(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M')
    return None

class password:
    # GET /password/foo HTTP/1.0
    def GET(self, arg=None):
        # Get query params
        query = web.input(
            bits = 6,
            words = 5
        )

        # Change output to JSON
        web.header('Content-type', 'application/json')

        # If no pattern at the end of the url, 
        # we will generate a random password
        if not arg:
            try:
                words = model.get_words(results = 2**int(query.bits))
                # Convert iterator
                wordlist = []
                for word in words:
                    wordlist.append(word.word)
            except(), e:
                web.internalerror(str(e))
                raise

            try:
                generatedPass = generate_password(
                    int(query.words), wordlist
                )
            except(), e:
                web.internalerror(str(e))
                raise

            web.ok()
            return json.dumps(dict(phrase=generatedPass))

        # Request for a pre-existing phrase
        phraseCode = base36decode(arg)

        try:
            phrase = model.get_phrase(base36decode(phraseCode))
            seqID = phrase.get('id')
        except(model.ModelError), e:
            web.notfound()
            return json.dumps(dict(error='not found'))
        except(), e:
            web.internalerror(str(e))
            raise

        # Update number of views
        try:
            model.update_phrase(seqID)
        except(), e:
            web.internalerror(str(e))
            raise

        # Get results from row
        results = {}
        results['phrase'] = phrase.get('phrase', None)
        results['code'] = phrase.get('code')
        results['created'] = phrase.get('created', None)
        results['maxdays'] = phrase.get('maxdays', 10)
        results['maxviews'] = phrase.get('maxviews', 10)
        results['views'] = phrase.get('views', 1)+1

        # Calculate if maxviews or maxdays has been reached
        deleteDate = results['created'] + timedelta(results['maxdays'])
        today = datetime.now()
        if today >= deleteDate or results['views'] >= results['maxviews']:
            try:
                deleted = model.delete_phrase(seqID)
            except:
                web.internalerror()
                raise

        # Return results to client
        web.ok()
        return json.dumps(results, default=dateHandler)

    # POST /password HTTP/1.0
    def POST(self):
        # Receive the passphrase through query params
        query = web.input(
            password = None,
            maxdays = 10,
            maxviews = 10
        )

        # Change output to JSON
        web.header('Content-type', 'application/json')

        # Generate unique code for phrase
        uuid = uuid4()
        phraseCode = str(uuid).split('-')[0]

        try:
            phraseid = model.add_phrase(
                phrase = query.password,
                code = base36decode(phraseCode),
                maxdays = int(query.maxdays),
                maxviews = int(query.maxviews)
            )
        except(model.ModelError), e:
            web.internalerror()
            return json.dumps(dict(error=str(e)))
        except(), e:
            web.internalerror()
            return json.dumps(dict(error=str(e)))

        web.created()
        return json.dumps(dict(
            phrase = query.password,
            code = phraseCode
        ))

    # DELETE /password/foo HTTP/1.0
    def DELETE(self, arg):
        # Change output to JSON
        web.header('Content-type', 'application/json')

        if not arg:
            web.internalerror()
            return json.dumps(dict(error='must have code'))

        try:
            phrase = model.get_phrase(code=base36decode(arg))
            seqID = phrase.get('id')
        except(), e:
            web.notfound()
            return json.dumps(dict(error='not found'))

        try:
            model.delete_phrase(seqID)
        except(), e:
            web.internalerror()
            return json.dumps(dict(error=str(e)))

        web.ok()
        return json.dumps(dict(status='%s deleted' % arg))
