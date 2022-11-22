from flaskapp.shared import *

from .model import Model

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
        self.wins = 0
        self.losses = 0