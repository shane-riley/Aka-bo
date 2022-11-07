import flask
from flask import abort, request
from flaskapp.storer import Storer
from google.cloud import datastore

# Define User
class User:
    """Model class for users (excludes epw)
    """
    def __init__(self, username="", email="", encrypted_password="", bio=""):
        self.username = username
        self.email = email
        self.encrypted_password = encrypted_password
        self.bio = bio

    

# Define User Storer
class UserStorer(Storer):
    """Storer class for users
    """

    KIND = 'User'
    
    def __init__(self):
        pass

    def put(self, user: User) -> User:
        return super().put(self.KIND, user)

    def get_by_username(self, username: str) -> User:
        return super().get_by_field(self.KIND, 'username', username)
        
        


# Define UserService
class UserService:
    """
    Service class for users
    """
    
    def __init__(self, user_storer: UserStorer):
        self.user_storer = user_storer
    
    def create_user(self, user: User):
        """
        Create user.

        Args:
            user (User): User to create

        Returns:
            user (User): User created

        Throws:
            Exception: If user missing required field (email, username, pw),
            or if user exists
        """

        # Make sure user's inputs exist
        # username, epw, email
        if not (user.username and user.email and user.encrypted_password):
            raise Exception

        # Check against db
        if self.user_storer.get_by_username(user.username):
            raise Exception

        # Add user
        return self.user_storer.put(user)


## SETUP ROUTES
from .__init__ import app, API_ROOT

user_storer = UserStorer()
user_service = UserService(user_storer)

# User API routes
# POST /user : Make a user
@app.route(API_ROOT+"/user", methods=['POST'])
def create_user():
    # Three inputs: email, username, encrypted PW
    # Check existence and then pass into service

    user = User(
        username            = request.args.get("username"),
        email               = request.args.get("email"),
        encrypted_password  = request.args.get("encrypted_password")     
    )

    # try:
    user_service.create_user(user)
    return flask.make_response("User Created.", 200)
    # except:
    #     return flask.make_response("User Creation Failed.", 500)
    
    

# GET /user/login: Login as user
@app.route(API_ROOT+"/user/login", methods=['GET'])
def login_user():

    # TODO: Smart firebase magic
    return flask.make_response("Not Implemented", 501)