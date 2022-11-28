from flask import jsonify, make_response, request
import typing

from flaskapp import Akabo
from flaskapp.models import User
from flaskapp.shared import *

def setup_user_api(app: Akabo):
    """
    Add user routes

    Args:
        app (Akabo): app to add to
    """

    # User API routes
    # GET /user : Load a user
    # Requires login, but can pull any user using their uid
    @app.route(API_ROOT+"/user", methods=['GET'])
    @check_token
    def get_user():
        # One input: uid (not necessarily the user's uid)
        # Get a user

        uid = request.args.get('uid')

        try:
            u = app.user_service.get_user(uid)
            return make_response(jsonify(u.serialize()), 200)
        except NoMatchException as e:
            print(e)
            return make_response("No Match Found.", 400)
        except InvalidInputException as e:
            print(e)
            return make_response("Invalid input.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)



    # POST /user : Make a user
    @app.route(API_ROOT+"/user", methods=['POST'])
    @check_token
    def create_user():
        # Three inputs: email, username, encrypted PW
        # Check existence and then pass into service

        user = User(
            username=request.args.get("username"),
            email=request.args.get("email"),
            uid=request.uid
        )

        try:
            u = app.user_service.create_user(user)
            return make_response(jsonify(u.serialize()), 200)
        except DuplicateException as e:
            print(e)
            return make_response("User already exists.", 400)
        except InvalidInputException as e:
            print(e)
            return make_response("Invalid input.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)

    # PUT /user : Modify a user
    @app.route(API_ROOT+"/user", methods=['PUT'])
    @check_token
    def update_user():
        # inputs: username and modifiable fields
        # bio

        user = User(
            username=request.args.get("username"),
            bio=request.args.get("bio"),
            uid=request.uid
        ) 

        try:
            u = app.user_service.update_user(user)
            return make_response(jsonify(u.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response("Invalid input.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)

    # DELETE /user : Delete a user
    @app.route(API_ROOT+"/user", methods=['DELETE'])
    @check_token
    def delete_user():
        # One input: uid (can only delete self)

        uid = request.uid

        try:
            u = app.user_service.delete_user(uid)
            return make_response(jsonify(u.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response("Invalid input.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)
