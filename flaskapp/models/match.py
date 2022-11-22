from datetime import datetime
import uuid

from flaskapp.shared import *
from .model import Model

class MatchTicket:
    """
    Model class for matchmaking tickets
    """

    KIND = 'Ticket'

    def __init__(self, 
                 username="",
                 game="", 
                 created=datetime.now().timestamp(),
                 polled=datetime.now().timestamp()):
        """
        Make a ticket model

        Args:
            username (str, optional): _description_. Defaults to "".
            game (str, optional): _description_. Defaults to "".
            created (float, optional): _description_. Defaults to datetime.now().timestamp().
        """

        self.username = username
        self.game = game
        self.created = created
        self.polled = polled
        self.expires = created + POLLING_TIMEOUT
        self.uuid = uuid.uuid4()
        self.gameuuid = ""
    
    def is_filled(self) -> bool:
        """
        Checks whether the ticket is filled

        Returns:
            bool: Whether game is filled
        """
        return len(self.gameuuid) > 0

    def touch(self):
        """
        Updates polled and expires times
        """
        ts = datetime.now().timestamp()
        self.polled = ts
        self.expires = ts + POLLING_TIMEOUT