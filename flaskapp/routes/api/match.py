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
    def create_ticket():
        # One input: username

        username = request.json.get("username")
        try:
            mt = app.match_service.create_ticket(username)
            return make_response(jsonify(mt.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response("Invalid input.", 400)
        except DuplicateException as e:
            print(e)
            return make_response("User already has ticket.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)

    # DELETE /matchmaking: Delete a ticket
    @app.route(API_ROOT+"/matchmaking", methods=['DELETE'])
    def delete_ticket():
        # One input: uuid

        uuid = request.args.get("uuid")
        try:
            mt = app.match_service.delete_ticket(uuid)
            return make_response(jsonify(mt.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response("Ticket not found.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)

    # GET /matchmaking: Poll a ticket
    @app.route(API_ROOT+"/matchmaking", methods=['GET'])
    def poll_ticket():
        # One input: uuid

        uuid = request.args.get("uuid")
        try:
            mt = app.match_service.poll_ticket(uuid)
            return make_response(jsonify(mt.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response("Ticket not found.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)
