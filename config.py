import os
_basedir = os.path.abspath(os.path.dirname(__file__))

THREADS_PER_PAGE = 8

DEBUG = False

HOST = '0.0.0.0'
PORT = 80

# both SECRET_KEY and CSRF_SESSION_KEY should  be overwridden in
# config_local
SECRET_KEY = "some_secret_key"
CSRF_SESSION_KEY = "some_other_secret_key"

CSRF_ENABLED = True

PRAW_USER_AGENT = "ror/0.0.1 by /u/hamms"

# Local overrides
try:
    from config_local import *
except ImportError as e:
    pass
