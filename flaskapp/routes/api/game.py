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
    @check_token
    def poll_game():

        # Inputs: game uuid and username
        uuid = request.args.get("uuid")
        uid = request.uid
        try:
            g = app.game_service.poll_game(uuid, uid)
            return make_response(jsonify(g.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response(jsonify({"message": "Invalid input."}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "Internal error."}), 500)

    # PUT /game: Make a move
    @app.route(API_ROOT+"/game", methods=['PUT'])
    @check_token
    def put_game():

        # Inputs: game uuid and username and move
        uuid = request.args.get("uuid")
        uid = request.uid
        move = request.args.get("move")

        try:
            g = app.game_service.make_move(uuid, uid, move)
            return make_response(jsonify(g.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response(jsonify({"message": "Invalid input."}), 400)
        except IllegalMoveException as e:
            print(e)
            return make_response(jsonify({"message": "Illegal move."}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "Internal error."}), 500)
    

    # DELETE /game: End game
    @app.route(API_ROOT+"/game", methods=['DELETE'])
    @check_token
    def ff_game():

        # Inputs: game uuid and username
        uuid = request.args.get("uuid")
        uid = request.uid

        try:
            g = app.game_service.forfeit_game(uuid, uid)
            return make_response(jsonify(g.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response(jsonify({"message": "Invalid input."}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "Internal error."}), 500)
