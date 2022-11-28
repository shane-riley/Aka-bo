from datetime import datetime, timezone
import uuid

from flaskapp.shared import *
from .model import Model

class MatchTicket(Model):
    """
    Model class for matchmaking tickets
    """

    KIND = 'Ticket'

    def __init__(self, 
                 uid="",
                 created=datetime.now(tz=timezone.utc),
                 polled=datetime.now(tz=timezone.utc)):
        """
        Make a ticket model

        Args:
            username (str, optional): _description_. Defaults to "".
            game (str, optional): _description_. Defaults to "".
            created (float, optional): _description_. Defaults to datetime.now().timestamp().
        """

        self.uid = uid  # User id
        self.created = created
        self.polled = polled
        self.expires = created + POLLING_TIMEOUT
        self.uuid = str(uuid.uuid4())  # Ticket id
        self.gameuuid = ""  # Game id
    
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
        ts = datetime.now(tz=timezone.utc)
        self.polled = ts
        self.expires = ts + POLLING_TIMEOUT