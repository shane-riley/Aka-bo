from flask import jsonify, make_response, request
import typing

from flaskapp import Akabo
from flaskapp.models import User
from flaskapp.shared import *

def setup_match_api(app: Akabo):
    """
    Add matchmaking routes

    Args:
        app (Akabo): app to add to
    """

    # POST /matchmaking: Make a ticket
    @app.route(API_ROOT+"/matchmaking", methods=['POST'])
    @check_token
    def create_ticket():
        # One input: uid from token

        uid = request.uid
        try:
            mt = app.match_service.create_ticket(uid)
            return make_response(jsonify(mt.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response(jsonify({"message": "Invalid input."}), 400)
        except DuplicateException as e:
            print(e)
            return make_response(jsonify({"message": "User has ticket."}), 400)
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "Internal error."}), 500)

    # DELETE /matchmaking: Delete a ticket
    @app.route(API_ROOT+"/matchmaking", methods=['DELETE'])
    @check_token
    def delete_ticket():
        # Two inputs: uuid and uid from token

        uuid = request.args.get("uuid")
        uid = request.uid
        try:
            mt = app.match_service.delete_ticket(uuid, uid)
            return make_response(jsonify(mt.serialize()), 200)
        except NoMatchException as e:
            print(e)
            return make_response(jsonify({"message": "No match found."}), 400)
        except UnauthorizedException as e:
            print(e)
            return make_response(jsonify({"message": "Unauthorized."}), 401)
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "Internal error."}), 500)

    # GET /matchmaking: Poll a ticket
    @app.route(API_ROOT+"/matchmaking", methods=['GET'])
    @check_token
    def poll_ticket():
        # Two inputs: uuid and uid from token

        uuid = request.args.get("uuid")
        uid = request.uid
        try:
            mt = app.match_service.poll_ticket(uuid, uid)
            return make_response(jsonify(mt.serialize()), 200)
        except NoMatchException as e:
            print(e)
            return make_response(jsonify({"message": "No match found."}), 400)
        except UnauthorizedException as e:
            print(e)
            return make_response(jsonify({"message": "Unauthorized."}), 401)
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "Internal error."}), 500)
