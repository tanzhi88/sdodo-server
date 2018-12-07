import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
TOKEN_EXPIRATION = 30 * 24 * 3600
DOMIAN = 'http://127.0.0.1:5000/'
DOMAIN_STATIC = 'http://127.0.0.1:5000/static'
BASE_PATH = basedir
STATIC_PATH = BASE_PATH + '/static/'