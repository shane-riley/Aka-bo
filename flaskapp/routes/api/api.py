import typing

from flaskapp import Akabo

from .game import setup_game_api
from .match import setup_match_api
from .user import setup_user_api

def setup_api(app: Akabo):
    """
    Set up API for flask application

    Args:
        app (Akabo): Akabo app
    """

    setup_game_api(app)
    setup_match_api(app)
    setup_user_api(app)

