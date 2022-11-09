from .__init__ import app, API_ROOT
import flask
from flask import abort, request, jsonify
from flaskapp.helpers import Store, Model, InvalidInputException, DuplicateException
from google.cloud import datastore
from typing import List

# Define User
class User(Model):
    """
    Model class for users
    """

    KIND = 'User'

    def __init__(self, username="", email="", encrypted_password="", bio=""):
        self.username = username
        self.email = email
        self.encrypted_password = encrypted_password
        self.bio = bio
        


# Define User Storer
class UserStore(Store):
    """
    Storer class for users using Google Cloud DataStore

    NOTE: Inherits Store for general methods
    """

    def __init__(self):
        pass

    def post_user(self, user: User) -> User:
        """
        Add a user to datastore

        Args:
            user (User): User to add

        Returns:
            User: User added
        """
        return super().post_object(User, user)

    def update_user(self, user: User) -> User:
        """
        Update user that exists

        Args:
            user (User): User to update

        Returns:
            User: User updated
        """
        return super().update_object(User, user, 'username', user.username)

    def get_by_username(self, username: str) -> List[User]:
        """
        Get a list of users matching the username

        Args:
            username (str): Username to match

        Returns:
            List[User]: Length=1 list of users
        """
        return super().get_objects_by_field(User, 'username', username)

    def delete_by_username(self, username: str) -> None:
        """
        Delete a list of users matching the username

        Args:
            username (str): Username to match

        Returns:
            List[User]: Length=1 list of users
        """
        return super().delete_by_field(User, 'username', username)[0]


# Define UserService
class UserService:
    """
    Service class for users.

    Contains business logic and all things not directly
    route or storage-oriented.
    """

    def __init__(self, user_store: UserStore):
        """
        Create a UserService

        Args:
            user_store (UserStore): Storage implementation to use
        """
        self.user_store = user_store

    def create_user(self, user: User) -> User:
        """
        Create user.

        Args:
            user (User): User to create

        Returns:
            user (User): User created

        Raises:
            DuplicateException: If username exists
            InvalidInputException: If other input issue
            Exception: Other errors
        """

        # Make sure user's inputs exist
        # username, epw, email
        if not (user.username and user.email and user.encrypted_password):
            raise InvalidInputException

        # Check against db
        if self.user_store.get_by_username(user.username):
            raise DuplicateException

        # Add user
        return self.user_store.post_user(user)

    def update_user(self, user: User) -> User:
        """
        Update user.

        Args:
            user (User): User to modify (username exists)

        Returns:
            user (User): User modified

        Raises:
            Exception: If user missing required field (email, username, pw),
            or if user exists
        """

        # Make sure user's inputs exist
        # username, epw, email
        if not (user.username):
            raise InvalidInputException

        # Check against db
        existing_user = self.user_store.get_by_username(user.username)[0]
        if not existing_user:
            raise InvalidInputException

        # Update modifiable fields
        existing_user.bio = user.bio
        return self.user_store.update_user(existing_user)

    def delete_user(self, username: str) -> User:
        """
        Delete user.

        Args:
            username (str): username to remove

        Returns:
            User: Removed user
        """

        # Check username doesn't exist
        if not self.user_store.get_by_username(username):
            raise InvalidInputException

        # Delete
        return self.user_store.delete_by_username(username)


# SETUP ROUTES

user_store = UserStore()
user_service = UserService(user_store)

# User API routes
# POST /user : Make a user
@app.route(API_ROOT+"/user", methods=['POST'])
def create_user():
    # Three inputs: email, username, encrypted PW
    # Check existence and then pass into service

    user = User(
        username=request.args.get("username"),
        email=request.args.get("email"),
        encrypted_password=request.args.get("encrypted_password")
    )

    try:
        u = user_service.create_user(user)
        return flask.make_response(jsonify(u.serialize()), 200)
    except DuplicateException as e:
        print(e)
        return flask.make_response("User already exists.", 400)
    except InvalidInputException as e:
        print(e)
        return flask.make_response("Invalid input.", 400)
    except Exception as e:
        print(e)
        return flask.make_response("Internal error.", 500)

# PUT /user : Modify a user
@app.route(API_ROOT+"/user", methods=['PUT'])
def update_user():
    # inputs: username and modifiable fields
    # bio

    user = User(
        username=request.args.get("username"),
        bio=request.args.get("bio")
    ) 

    try:
        u = user_service.update_user(user)
        return flask.make_response(jsonify(u.serialize()), 200)
    except InvalidInputException as e:
        print(e)
        return flask.make_response("Invalid input.", 400)
    except Exception as e:
        print(e)
        return flask.make_response("Internal error.", 500)

# DELETE /user : Delete a user
@app.route(API_ROOT+"/user", methods=['DELETE'])
def delete_user():
    # One input: username

    username = request.args.get("username")

    try:
        u = user_service.delete_user(username)
        return flask.make_response(jsonify(u.serialize()), 200)
    except InvalidInputException as e:
        print(e)
        return flask.make_response("Invalid input.", 400)
    except Exception as e:
        print(e)
        return flask.make_response("Internal error.", 500)


# GET /user/login: Login as user
@app.route(API_ROOT+"/user/login", methods=['GET'])
def login_user():

    # TODO: Smart firebase magic
    return flask.make_response("Not Implemented", 501)
