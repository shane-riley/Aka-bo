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
    # POST /user : Make a user
    @app.route(API_ROOT+"/user", methods=['POST'])
    def create_user():
        # Three inputs: email, username, encrypted PW
        # Check existence and then pass into service

        user = User(
            username=request.json.get("username"),
            email=request.json.get("email"),
            encrypted_password=request.json.get("encrypted_password")
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
    def update_user():
        # inputs: username and modifiable fields
        # bio

        user = User(
            username=request.json.get("username"),
            bio=request.json.get("bio")
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
    def delete_user():
        # One input: username

        username = request.args.get("username")

        try:
            u = app.user_service.delete_user(username)
            return make_response(jsonify(u.serialize()), 200)
        except InvalidInputException as e:
            print(e)
            return make_response("Invalid input.", 400)
        except Exception as e:
            print(e)
            return make_response("Internal error.", 500)


    # GET /user/login: Login as user
    @app.route(API_ROOT+"/user/login", methods=['GET'])
    def login_user():

        # TODO: Smart firebase magic
        return make_response("Not Implemented", 501)
