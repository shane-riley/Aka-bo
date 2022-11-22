class MatchTicketService:
    
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