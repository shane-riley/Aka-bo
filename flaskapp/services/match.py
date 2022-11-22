from flaskapp.models import Game, MatchTicket
from flaskapp.shared import *
from flaskapp.stores import GameStore, MatchStore, UserStore

from .service import Service

class MatchService(Service):
    
    def __init__(self, game_store: GameStore, match_store: MatchStore):
        """
        Create a MatchService

        Args:
            match_store (MatchStore): Storage implementation to use
        """
        self.game_store = game_store
        self.match_store = match_store

    # Create a ticket
    def create_ticket(self, username: str) -> MatchTicket:
        """
        Create a matchmaking ticket

        Args:
            username (str): User looking for game
        
        Returns:
            MatchTicket: Matchmaking ticket
        
        Throws:
            DuplicateException: If username already has ticket
            InvalidInputException: If other input issue
            Exception: Other errors
        """

        # Make the ticket
        ticket = MatchTicket(username=username)
        
        # Make sure no existing tickets under username (excluding filled tickets)
        if list(filter(lambda tix: tix.gameuuid == "", self.match_store.get_by_username(ticket.username))):
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

        # Ticket exists
        if not ticket:
            raise InvalidInputException

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
        matched_ticket = next(filter(lambda tix: tix.username != ticket.username, other_tickets), None)

        if not matched_ticket:
            # Nothing to do; touch
            ticket.touch()
            return self.match_store.update_ticket(ticket)

        # else
        # Make a Game instance and point both tickets at it
        player_one = ticket.username
        player_two = matched_ticket.username
        game = Game(player_one=player_one, player_two=player_two)

        # Store game
        self.game_store.post_game(game)

        # Mark tickets
        ticket.gameuuid = game.uuid
        matched_ticket.gameuuid = game.uuid
        ticket.touch()

        # Save the marked tickets
        self.match_store.update_ticket(matched_ticket)
        return self.match_store.update_ticket(ticket)



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

        # Ticket exists
        if not ticket:
            raise InvalidInputException

        # No-op if ticket is filled
        if ticket.is_filled():
            return ticket
        
        # else
        # Drop ticket
        # NOTE: There is 100% a race condition here:
        # Match could be filled after checking and before deleting
        # Treating this as unlikely for now and as a TODO
        return self.match_store.delete_by_uuid(uuid)