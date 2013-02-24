import web
from os.path import join, abspath, dirname

# Helpful functions for relative paths
here = lambda *p: join(abspath(dirname(__file__)), *p)
PROJECT_ROOT = here('.') # settings.py is in PROJECT_ROOT already
root = lambda *p: join(abspath(PROJECT_ROOT), *p)

web.config.debug = True

TEMPLATE_DIR = root('templates')
STATIC_DIR = root('static')
I18N_DIR = root('i18n')
LOCALE = 'sv_SE'

DB_ENGINE = 'postgres'
DB_HOST = 'goto'
DB_NAME = 'passwordfrank'
DB_USER = 'nocturnal'
DB_PASS = 'wad93Pmne7toMiV6O6h8yw'

# Some UI stuff
APP_NAME = 'Password Pusher'

# Some helper functions required globally
# Generate random passphrase from wordlist
def generate_password(nwords=None, words=None):
    from random import SystemRandom

    if not isinstance(words, list):
        raise TypeError('Requires list argument')

    choice = SystemRandom().choice

    return ' '.join(choice(words) for num in range(nwords))

# Base36 encoder from Wikipedia :)
def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    if not isinstance(number, (int, long)):
        raise TypeError('First argument must be number')

    base36 = ''
    sign = ''

    # Negatives
    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign+alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign+base36

# Base36 decoder
def base36decode(number):
    return int(number, 36)

