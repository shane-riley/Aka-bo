import flask
from flask import abort, request
from flaskapp.helpers import Store, InvalidInputException, DuplicateException, SUPPORTED_GAMES
from google.cloud import datastore
from datetime import datetime
from typing import List, Optional
import uuid
from .__init__ import app, API_ROOT
from .game import GameStore

POLLING_TIMEOUT = 30
# Match ticket model
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

# Match ticket storer
class MatchStore(Store):

    def post_ticket(self, ticket: MatchTicket) -> MatchTicket:
        """
        Add a ticket to datastore

        Args:
            ticket (MatchTicket): Ticket to add

        Returns:
            MatchTicket: Ticket added
        """
        return super().post_object(MatchTicket, ticket)

    def update_ticket(self, ticket: MatchTicket) -> MatchTicket:
        """
        Update a ticket that exists

        Args:
            ticket (MatchTicket): Ticket to update

        Returns:
            MatchTicket: Ticket updated
        """
        
        # Ticket uuid is the key
        return super().update_object(MatchTicket, ticket, 'uuid', ticket.uuid)
    
    def get_by_uuid(self, uuid: str) -> Optional[MatchTicket]:
        """
        Get Ticket matching uuid or None

        Args:
            uuid (str): Unique identifier

        Returns:
            Optional[MatchTicket]: MatchTicket or None
        """
        return super().get_object_by_field(MatchTicket, 'uuid', uuid)

    def get_by_username(self, username: str) -> List[MatchTicket]:
        """
        Get user's matchmaking tickets (valid only)

        Args:
            username (str): username

        Returns:
            List[MatchTicket]: MatchTickets for username
        """
        return super().get_objects_by_field(MatchTicket, 'username', username)

    def delete_by_uuid(self, uuid: str) -> Optional[MatchTicket]:
        """
        Delete Ticket matching uuid or None

        Args:
            uuid (str): Unique identifier

        Returns:
            Optional[MatchTicket]: MatchTicket or None
        """
        return super().delete_by_field(MatchTicket, 'uuid', uuid)[0]
    
    def get_valid_tickets(self) -> List[MatchTicket]:
        """
        Get list of existing non-expired tickets

        Returns:
            List[MatchTicket]: List of non-expired tickets
        """
        return super().get_objects(MatchTicket)

# Match ticket Service
class MatchService:
    
    def __init__(self, match_store: MatchStore):
        """
        Create a MatchService

        Args:
            match_store (MatchStore): Storage implementation to use
        """
        self.match_store = match_store

    # Create a ticket
    def create_ticket(self, ticket: MatchTicket) -> MatchTicket:
        """
        Create a matchmaking ticket

        Args:
            username (str): User looking for game
            game (str): Game to play
        
        Returns:
            MatchTicket: Matchmaking ticket
        
        Throws:
            DuplicateException: If username already has ticket
            InvalidInputException: If other input issue
            Exception: Other errors
        """
    
        # Make sure nonzero username
        if not ticket.username:
            raise InvalidInputException
        
        # Make sure no existing tickets under username
        if self.match_store.get_by_username(ticket.username):
            raise DuplicateException

        # Make the ticket
        return self.match_store.post_ticket(ticket)
        
    # Poll a ticket
    def poll_ticket(self, uuid: str) -> MatchTicket:
        """
        Poll MatchTicket

        Args:
            uuid (str): uuid to poll

        Returns:
            MatchTicket: Current MatchTicket
        """

        # Grab the ticket
        ticket = self.match_store.get_by_uuid(uuid)

        # If ticket is filled nothing to do
        if ticket.is_filled():
            # Nothing to do; touch
            ticket.touch()
            return self.match_store.update_ticket(ticket)

        # else
        # Attempt to fill ticket
        # NOTE: There is a race condition here:
        # What if the ticket gets filled right before we fill it?
        # Treating this as unlikely for now and as a TODO
        other_tickets = self.match_store.get_valid_tickets()
        ticket_to_match = next(filter(lambda tix: tix.username != ticket.username, other_tickets), None)

        if not ticket_to_match:
            # Nothing to do; touch
            ticket.touch()
            return self.match_store.update_ticket(ticket)

        # else
        # Make a Game instance and point both tickets at it
        # TODO



    # Delete a ticket
    def delete_ticket(self, uuid: str) -> MatchTicket:
        """
        Delete MatchTicket.

        No-ops if match has already been created

        Args:
            uuid (str): uuid to remove

        Returns:
            MatchTicket: Removed MatchTicket
        """

        # Grab the ticket
        ticket = self.match_store.get_by_uuid(uuid)

        # No-op if ticket is filled
        if ticket.is_filled():
            return ticket
        
        # else
        # Drop ticket
        # NOTE: There is 100% a race condition here:
        # Match could be filled after checking and before deleting
        # Treating this as unlikely for now and as a TODO
        self.match_store.delete_by_uuid(uuid)
        


match_store = MatchStore()
# NOTE: I can only reinstantiate this not as a singleton
# Since the datastore client underpinning it is a singleton
# game_store = GameStore() # TODO: fix a circular import
# match_service = MatchService(match_store, game_store)

# Add matchmaking api routes
# POST /matchmaking : Make a ticket
# GET /matchmaking/{ticketid} : Poll a ticket
# DELETE /matchmaking : Drop a ticket
