from flask import jsonify, make_response, request
import typing

from flaskapp import Akabo
from flaskapp.models import User
from flaskapp.shared import *

def setup_game_api(app: Akabo):
    """
    Add game routes

    Args:
        app (Akabo): app to add to
    """

    # GET /game: Poll game
    @app.route(API_ROOT+"/game", methods=['GET'])
    def poll_game():

        # Inputs: game uuid and username
        uuid = request.args.get("uuid")
        username = request.args.get("username")
        try:
            g = app.game_service.poll_game(uuid, username)
            return make_response(jsonify(g.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response("Invalid input.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)

    # PUT /game: Make a move
    @app.route(API_ROOT+"/game", methods=['PUT'])
    def put_game():

        # Inputs: game uuid and username and move
        uuid = request.json.get("uuid")
        username = request.json.get("username")
        move = request.json.get("move")

        try:
            g = app.game_service.make_move(uuid, username, move)
            return make_response(jsonify(g.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response("Invalid input.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)
    

    # DELETE /game: End game
    @app.route(API_ROOT+"/game", methods=['DELETE'])
    def ff_game():

        # Inputs: game uuid and username
        uuid = request.args.get("uuid")
        username = request.args.get("username")

        try:
            g = app.game_service.forfeit_game(uuid, username)
            return make_response(jsonify(g.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response("Invalid input.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)