from datetime import timedelta
from functools import wraps
from flask import request, make_response
from firebase_admin import auth

# Various exceptions for global use
class DuplicateException(Exception):
    pass

class IllegalMoveException(Exception):
    pass

class InvalidInputException(Exception):
    pass

# jwt auth handler
def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get('authorization'):
            return make_response("Unauthorized.", 401)
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return make_response("Unauthorized.", 401)
        return f(*args, **kwargs)
    return wrap


# API ROOT
API_ROOT = "/api/v1"

# NCOL, NROW
NCOL = 7
NROW = 6
NCONNECT = 4

# Timeouts
GAME_TIMEOUT = timedelta(hours=1)
POLLING_TIMEOUT = timedelta(hours=1)
# GAME_TIMEOUT = timedelta(seconds = 120)
# POLLING_TIMEOUT = timedelta(seconds = 30)