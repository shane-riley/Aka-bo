from datetime import timedelta

# Various exceptions for global use
class DuplicateException(Exception):
    pass

class IllegalMoveException(Exception):
    pass

class InvalidInputException(Exception):
    pass

# API ROOT
API_ROOT = "/api/v1"

# NCOL, NROW
NCOL = 7
NROW = 6
NCONNECT = 4

# Timeouts
GAME_TIMEOUT = timedelta(seconds = 120)
POLLING_TIMEOUT = timedelta(seconds = 30)