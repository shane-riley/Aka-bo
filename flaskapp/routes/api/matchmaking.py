import flask
from flask import abort, request
from flaskapp.helpers import Store, InvalidInputException, DuplicateException, SUPPORTED_GAMES
from google.cloud import datastore
from datetime import datetime
from typing import List, Optional
import uuid
from .__init__ import app, API_ROOT
from .game import GameStore

POLLING_TIMEOUT = 30
# Match ticket model


# Match ticket storer


# Match ticket Service

        


match_store = MatchStore()
# NOTE: I can only reinstantiate this not as a singleton
# Since the datastore client underpinning it is a singleton
# game_store = GameStore() # TODO: fix a circular import
# match_service = MatchService(match_store, game_store)

# Add matchmaking api routes
# POST /matchmaking : Make a ticket
# GET /matchmaking/{ticketid} : Poll a ticket
# DELETE /matchmaking : Drop a ticket
