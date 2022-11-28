from flaskapp.models import Game, MatchTicket
from flaskapp.shared import *
from flaskapp.stores import GameStore, MatchStore, UserStore

from .service import Service

class MatchService(Service):
    
    def __init__(self, game_store: GameStore, match_store: MatchStore, user_store: UserStore):
        """
        Create a MatchService

        Args:
            game_store (GameStore): Storage for games
            match_store (MatchStore): Storage for tickets
            user_store (UserStore): Storage for users
        """
        self.game_store = game_store
        self.match_store = match_store
        self.user_store = user_store

    # Create a ticket
    def create_ticket(self, uid: str) -> MatchTicket:
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

        # Check uid exists
        if not self.user_store.uid_exists(uid):
            raise InvalidInputException

        # Make the ticket
        ticket = MatchTicket(uid=uid)
        
        # Make sure no existing tickets under username (excluding filled tickets)
        if list(filter(lambda tix: tix.gameuuid == "", self.match_store.get_by_uid(ticket.uid))):
            raise DuplicateException

        # Make the ticket
        return self.match_store.post_ticket(ticket)
        
    # Poll a ticket
    def poll_ticket(self, uuid: str, uid: str) -> MatchTicket:
        """
        Poll MatchTicket

        Args:
            uuid (str): uuid to poll
            uid (str): user id

        Returns:
            MatchTicket: Current MatchTicket
        """

        # Grab the ticket
        ticket = self.match_store.get_by_uuid(uuid)

        # Ensure ticket
        if not ticket:
            raise NoMatchException

        # Ensure authorization
        if not uid == ticket.uid:
            raise UnauthorizedException

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
        matched_ticket = next(filter(lambda tix: tix.uid != ticket.uid and not tix.gameuuid, other_tickets), None)

        if not matched_ticket:
            # Nothing to do; touch
            ticket.touch()
            return self.match_store.update_ticket(ticket)

        # else
        # Make a Game instance and point both tickets at it
        player_one = ticket.uid
        player_two = matched_ticket.uid
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
    def delete_ticket(self, uuid: str, uid: str) -> MatchTicket:
        """
        Delete MatchTicket.

        No-ops if match has already been created

        Args:
            uuid (str): uuid to remove
            uid (str): unique user identified

        Returns:
            MatchTicket: Removed MatchTicket
        """

        # Grab the ticket
        ticket = self.match_store.get_by_uuid(uuid)

        if not ticket:
            raise NoMatchException

        if uid != ticket.uid:
            raise UnauthorizedException

        # No-op if ticket is filled
        if ticket.is_filled():
            return ticket
        
        # else
        # Drop ticket
        # NOTE: There is 100% a race condition here:
        # Match could be filled after checking and before deleting
        # Treating this as unlikely for now and as a TODO
        return self.match_store.delete_by_uuid(uuid)