import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

TOKEN_EXPIRATION = 30 * 24 * 3600
BASE_PATH = basedir
STATIC_PATH = BASE_PATH + '/static/'