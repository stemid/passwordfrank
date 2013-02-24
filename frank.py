import gettext
import web

import ui, api, settings

# Prepare localization
gettext.install('messages', settings.I18N_DIR, unicode=True)
gettext.translation(
    'messages', 
    settings.I18N_DIR, 
    languages=[
        settings.LOCALE
    ]
).install(True)

urls = (
    '/password', 'api.password',
    '/password/(.+)', 'api.password',
    '/', 'ui.index',
    '/(.+)', 'ui.index',
)

app = web.application(urls, globals())

if web.config.debug is False:
    app.internalerror = ui.internalerror

if __name__ == '__main__':
    app.run()

if __name__.startswith('_mod_wsgi_'):
    application = app.wsgifunc()
