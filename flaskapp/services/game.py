from datetime import datetime, timezone

from flaskapp.models import Game, GameState
from flaskapp.shared import *
from flaskapp.stores import GameStore, UserStore

from .service import Service

class GameService(Service):
    
    def __init__(self, game_store: GameStore, user_store: UserStore):
        """
        Create a GameService

        Args:
            game_store (GameStore): Game store instance
            user_store (UserStore): User store instance
        """
        self.game_store = game_store
        self.user_store = user_store

    # Log win
    def log_win(self, uid: str):
        """
        Add to win counter

        Args:
            uid (str): unique user identifier

        Returns:
            User: updated user object
        """

        # Get user
        user = self.user_store.get_by_uid(uid)
        # User exists
        if not user:
            raise Exception
        user.wins = user.wins + 1
        return self.user_store.update_user(user)

    # Log loss
    def log_loss(self, uid: str):
        """
        Add to loss counter

        Args:
            uid (str): unique user identifier

        Returns:
            User: updated user object
        """

        # Get user
        user = self.user_store.get_by_uid(uid)
        # User exists
        if not user:
            raise Exception
        user.losses = user.losses + 1
        return self.user_store.update_user(user)

    # Create Game
    def create_game(self, player_one: str, player_two: str) -> Game:
        """
        Make a new game

        Args:
            player_one (str): Player one uid
            player_two (str): Player two uid
        
        Returns:
            game (Game): Game created

        Raises:
            InvalidInputException: If input issue
        """

        # Ensure uids are valid
        if not self.user_store.uid_exists(player_one):
            raise InvalidInputException
        if not self.user_store.uid_exists(player_two):
            raise InvalidInputException

        # Make a new game
        game = Game(
            player_one=player_one,
            player_two=player_two
        )

        # Store the game
        return self.game_store.post_game(game)

    # Make move
    def make_move(self, uuid: str, uid: str, move: str) -> Game:
        """
        Make a move

        Args:
            uuid (str): Game uuid
            uid (str): User making move
            move (str): Move to make (column)

        Returns:
            Game: New Game object
        """

        # Grab game using uuid
        with self.game_store.get_client().transaction():
            game = self.game_store.get_by_uuid(uuid)

            # Cast
            move = int(move)

            # Ensure Game exists
            if not game:
                raise InvalidInputException

            # Ensure uid in game
            if uid not in [game.player_one, game.player_two]:
                raise InvalidInputException

            # Ensure user is correct player
            if uid == game.player_one and GameState(game.state) != GameState.MOVE_ONE:
                raise InvalidInputException
            if uid == game.player_two and GameState(game.state) != GameState.MOVE_TWO:
                raise InvalidInputException

            # Player is authorized to move

            # Check legality of move
            if not game.is_legal(move):
                raise IllegalMoveException

            # Update the game with the move
            game.apply_move(move)

            if GameState(game.state) == GameState.WIN_ONE:
                self.log_win(game.player_one)
                self.log_loss(game.player_two)
            if GameState(game.state) == GameState.WIN_TWO:
                self.log_win(game.player_two)
                self.log_loss(game.player_one)

            # Touch
            if uid == game.player_one:
                game.touch_1()
            if uid == game.player_two:
                game.touch_2()

            # Update and return
            return self.game_store.update_game(game)

    # Forfeit game
    def forfeit_game(self, uuid: str, uid: str) -> Game:
        """
        Forfeit game

        Args:
            uuid (str): Game uuid
            uid (str): uid attempting forfeit

        Returns:
            Game: Game forfeited

        Raises:
            InvalidInputException: If uid cannot ff at this time,
            or if user not in game
        """

        # Grab game using uuid
        with self.game_store.get_client().transaction():
            game = self.game_store.get_by_uuid(uuid)

            # Ensure Game exists
            if not game:
                raise InvalidInputException

            # Ensure uid in game
            if uid not in [game.player_one, game.player_two]:
                raise InvalidInputException

            # Can only ff if it is the player's move
            if uid == game.player_one and GameState(game.state) != GameState.MOVE_ONE:
                raise InvalidInputException
            if uid == game.player_two and GameState(game.state) != GameState.MOVE_TWO:
                raise InvalidInputException

            # ff is valid
            if uid == game.player_one:
                game.state = GameState.FF_ONE.value
                self.log_loss(game.player_one)
                self.log_win(game.player_two)
                game.touch_1()
            if uid == game.player_two:
                game.state = GameState.FF_TWO.value
                self.log_loss(game.player_two)
                self.log_win(game.player_win)
                game.touch_2()
            
            # Update and return
            return self.game_store.update_game(game)

    # Poll for update 
    def poll_game(self, uuid: str, uid: str) -> Game:
        """
        Poll game for update

        Args:
            uuid (str): uuid of game
            uid (str): uid of player

        Returns:
            Game: updated game object
        """

        # Grab game using uuid
        with self.game_store.get_client().transaction():
            game = self.game_store.get_by_uuid(uuid)

            # Ensure Game exists
            if not game:
                raise InvalidInputException

            # Ensure uid in game
            if uid not in [game.player_one, game.player_two]:
                raise InvalidInputException
            
            # Touch and check for timeout
            if uid == game.player_one:
                game.touch_1()
                if game.player_two_expires < datetime.now(tz=timezone.utc):
                    game.state = GameState.TIMEOUT_TWO.value
                    self.log_loss(game.player_two)
                    self.log_win(game.player_one)
            if uid == game.player_two:
                game.touch_2()
                if game.player_one_expires < datetime.now(tz=timezone.utc):
                    game.state = GameState.TIMEOUT_ONE.value
                    self.log_loss(game.player_one)
                    self.log_win(game.player_two)
            
            # Store and return
            # TODO: wicked evil race condition happening rn
            # return self.game_store.update_game(game)
            return game
