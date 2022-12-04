from flaskapp.shared import *

from .model import Model

class User(Model):
    """
    Model class for users
    """
    KIND = 'User'

    def __init__(self, uid="", username="", email="", bio=""):
        self.uid = uid  # PRIMARY IDENTIFIER
        self.username = username
        self.email = email
        self.bio = bio
        self.wins = 0
        self.losses = 0