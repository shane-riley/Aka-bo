from datetime import timedelta
from functools import wraps
from flask import jsonify, request, make_response
from firebase_admin import auth

# API ROOT
API_ROOT = "/api/v1"

# NCOL, NROW
NCOL = 7
NROW = 6
NCONNECT = 4

# AUTH
DO_AUTHORIZATION = False

# Various exceptions for global use

# Duplicate exception
class DuplicateException(Exception):
    pass

# Illegal moves (game only)
class IllegalMoveException(Exception):
    pass

# General invalid input exception
class InvalidInputException(Exception):
    pass

# No match found
class NoMatchException(Exception):
    pass

# Not authorized
class UnauthorizedException(Exception):
    pass

# jwt auth handler
def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if DO_AUTHORIZATION:
            if not request.headers.get('authorization'):
                return make_response(jsonify({"message": "Unauthorized."}), 401)
            try:
                uid = auth.verify_id_token(request.headers['authorization'])
                request.uid = uid
            except:
                return make_response(jsonify({"message": "Unauthorized."}), 401)
        else:
            request.uid = request.args.get('uid')
            if not request.uid:
                request.uid = request.args.get('username')
        return f(*args, **kwargs)
    return wrap


# Timeouts
GAME_TIMEOUT = timedelta(hours=1)
POLLING_TIMEOUT = timedelta(hours=1)
# GAME_TIMEOUT = timedelta(seconds = 120)
# POLLING_TIMEOUT = timedelta(seconds = 30)