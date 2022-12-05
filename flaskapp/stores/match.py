from typing import List, Optional

from flaskapp.models import MatchTicket
from .store import Store

class MatchStore(Store):
    """
    Class for storing MatchTickets

    Inherits from Store
    """

    def __init__(self, client):
        super().__init__(client)

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
        Get Ticket matching uuid or None if no matches

        Args:
            uuid (str): Unique identifier

        Returns:
            Optional[MatchTicket]: MatchTicket or None
        """
        return super().get_object_by_field(MatchTicket, 'uuid', uuid)

    def get_by_uid(self, uid: str) -> List[MatchTicket]:
        """
        Get user's matchmaking tickets (valid only)

        Args:
            uid (str): user id

        Returns:
            List[MatchTicket]: MatchTickets for user id
        """
        return super().get_objects_by_field(MatchTicket, 'uid', uid)

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