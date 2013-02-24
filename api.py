from datetime import datetime, timedelta
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
        seqID = base36decode(arg)

        try:
            phrase = model.get_phrase(seqID)
        except(model.ModelError), e:
            web.notfound(str(e))
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

        try:
            phraseid = model.add_phrase(
                query.password,
                int(query.maxdays),
                int(query.maxviews)
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
            id = base36encode(phraseid)
        ))

    # DELETE /password/foo HTTP/1.0
    def DELETE(self, arg):
        if not arg:
            web.internalerror()
            return json.dumps(dict(error='must have id'))

        # Change output to JSON
        web.header('Content-type', 'application/json')

        try:
            model.delete_phrase(base36decode(arg))
        except(), e:
            web.internalerror()
            return json.dumps(dict(error=str(e)))

        web.ok()
        return json.dumps(dict(status='%s deleted' % arg))
