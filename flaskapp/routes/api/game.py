from enum import Enum
from typing import List, Optional
import flask
import uuid
from datetime import datetime
from flaskapp.routes.api.user import UserStore
from helpers import SUPPORTED_GAMES, InvalidInputException
from .__init__ import app

GAME_TIMEOUT = 120

class GameState(Enum):
    """
    GameState Enum

    Stored as integers in datastore
    """
    MOVE_ONE = 1 # Moves
    MOVE_TWO = 2
    WIN_ONE = 3 # Wins
    WIN_TWO = 4
    DRAW = 5 # draw
    TIMEOUT_ONE = 6 # timeouts
    TIMEOUT_TWO = 7
    FF_ONE = 8 # forfeits
    FF_TWO = 9
    
class Connect4:
    """
    Class with helper methods for managing board states

    """
    
    @staticmethod
    def is_reasonable(move: str) -> bool:
        """
        Ensure move is a reasonable column

        Args:
            move (str): move to consider

        Returns:
            bool: whether move is reasonable
        """

        try:
            col = int(move)
            if col < 0 or col > 6:
                return False
        except:
            return False
        return True

    @staticmethod
    def is_legal(board: str, move: str) -> bool:
        """
        Ensure move can be applied to game board

        Args:
            board (str): Current board state
            move (str): move to consider

        Returns:
            bool: whether move is legal
        """

        if not Connect4.is_legal(move):
            return False
        
        # There are 6 rows per column:
        # If this column already appears 6 times move is not legal
        if board.count(move) >= 6:
            return False
        
        return True
    
    @staticmethod
    def apply_move(board: str, move: str) -> str:
        """
        Apply a move to the board

        Args:
            board (str): Current board state
            move (str): move to add

        Returns:
            str: New board state
        """
        board = board + move
        return board

    @staticmethod
    def check_end(board: str) -> GameState:
        """
        Check for game end

        Args:
            board (str): Current board state

        Returns:
            GameState: Appropriate state (excludes forfeits and timeouts)
        """

        # Check for win
        # TODO

        # No win; check for draw
        if len(board) >= 6*7:
            return GameState.DRAW

        # No end; get next player
        if (len(board)%2):
            return GameState.MOVE_ONE
        else:
            return GameState.MOVE_TWO


# Game model
class Game:
    """
    Generic class for games
    NOTE: only two-player games at the moment

    Another NOTE: Game is currently restricted to using only primitive types
    (see how board is string and state steals the value of the enum)
    This decision is mostly because storing objects would make trouble with Datastore unpacking,
    but certainly would be best down the road. For now however, member variables are elevated from their
    primitive types only when necessary
    """

    KIND = 'Game'

    def __init__(self,
                 game_type="",
                 created=datetime.now().timestamp(),
                 player_one="",
                 player_two="",
                 board="",
                 state=GameState.MOVE_ONE.value):
        """
        Creates a game

        Args:
            game_type (str, optional): Game type. Defaults to "C4".
            created (float, optional): Time of creation. Defaults to datetime.now().timestamp().
            player_one (str, optional): Player one username. Defaults to "".
            player_two (str, optional): Player two username. Defaults to "".
            board (Board, optional): Board layout as string. Defaults to "".
            state (GameState, optional): State of game. Defaults to GameState.MOVE_ONE.value.
        """

        self.game_type = game_type
        self.uuid = uuid.uuid4()
        self.created = created
        self.player_one = player_one
        self.player_two = player_two
        self.board=board,
        self.state=state,
        self.player_one_polled = created
        self.player_two_polled = created
        self.player_one_expires = created + GAME_TIMEOUT
        self.player_two_expires = created + GAME_TIMEOUT

    def touch_1(self):
        """
        Updates Player 1
        """
        n = datetime.now.timestamp()
        self.player_one_polled = n
        self.player_one_expires = n + GAME_TIMEOUT

    def touch_2(self):
        """
        Updates Player 2
        """
        n = datetime.now.timestamp()
        self.player_one_polled = n
        self.player_one_expires = n + GAME_TIMEOUT

    def complete(self) -> bool:
        """
        Return true iff game is over

        Returns:
            bool: Game is over
        """
        return GameState(self.state) not in [GameState.MOVE_ONE, GameState.MOVE_TWO]
    
class GameStore:
    """
    Class for storing Games
    """
    
    def post_game(self, game: Game) -> Game:
        """
        Add a game to datastore

        Args:
            game (Game): Game to add

        Returns:
            Game: Game added
        """
        return super().post_object(Game, game)

    def update_game(self, game: Game) -> Game:
        """
        Update a game that exists

        Args:
            game (Game): Game to update

        Returns:
            Game: Game updated
        """

        # Game uuid is the key
        return super().update_object(Game, game, 'uuid', game.uuid)

    def get_by_uuid(self, uuid: str) -> Optional[Game]:
        """
        Get Game matching uuid or None if no matches

        Args:
            uuid (str): Unique identifier

        Returns:
            Optional[Game]: Game or None
        """
        return super().get_object_by_field(Game, 'uuid', uuid)
    
    def get_by_username(self, username: str) -> List[Game]:
        """
        Get user's games

        Args:
            username (str): username

        Returns:
            List[Game]: Games for username
        """
        return super().get_objects_by_field(Game, 'player_one', username).extend(
               super().get_objects_by_field(Game, 'player_two', username))
    
    def delete_by_uuid(self, uuid: str) -> Optional[Game]:
        """
        Delete Game matching uuid or None

        Args:
            uuid (str): Unique identifier

        Returns:
            Optional[Game]: Game or None
        """
        return super().delete_by_field(Game, 'uuid', uuid)[0]

class GameService:
    
    def __init__(self, game_store: GameStore, user_store: UserStore):
        """
        Create a GameService

        Args:
            game_store (GameStore): Game store instance
            user_store (UserStore): User store instance
        """
        self.game_store = game_store
        self.user_store = user_store

    # Create Game
    def create_game(self, game_type: str, player_one: str, player_two: str) -> Game:
        """
        Make a new game

        Args:
            game_type (str): Type to play
            player_one (str): Player one username
            player_two (str): Player two username
        
        Returns:
            game (Game): Game created

        Raises:
            InvalidInputException: If input issue
        """

        # Ensure game_type is valid
        if game_type not in SUPPORTED_GAMES:
            raise InvalidInputException

        # Ensure usernames are valid
        if not self.user_store.get_by_username(player_one):
            raise InvalidInputException
        if not self.user_store.get_by_username(player_two):
            raise InvalidInputException

        # Make a new game
        game = Game(
            game_type=game_type,
            player_one=player_one,
            player_two=player_two
        )

        # Store the game
        return self.game_store.post_game(game)

    # Make move
    def make_move(self, uuid: str, username: str, move: str) -> Game:
        """
        Make a move

        Args:
            uuid (str): Game uuid
            username (str): User making move
            move (str): Move to make (column)

        Returns:
            Game: New Game object
        """

        # Grab game using uuid
        game = self.game_store.get_by_uuid(uuid)

        # Ensure username in game
        if username not in [game.player_one, game.player_two]:
            raise InvalidInputException

        # Ensure user is the one to move
        if ((username == game.player_one and 
            GameState(game.state) != GameState.MOVE_ONE)
            or (username == game.player_two and 
            GameState(game.state) != GameState.MOVE_TWO)):
            raise InvalidInputException

        # Ensure move is legal
        if not Connect4.is_legal(game.board, move):
            raise InvalidInputException

        # Apply move
        new_board = Connect4.apply_move(game.board, move)

        # Check for a win
        new_state = Connect4.check_end(new_board).value

        # Touch
        if GameState(game.state) == GameState.MOVE_ONE:
            game.touch_1()
        else:
            game.touch_2()

        # Update values
        game.board = new_board
        game.state = new_state

        # Update datastore
        return self.game_store.update_game(game)

    # Forfeit game
    def forfeit_game(self, uuid: str, username: str) -> Game:
        """
        Forfeit game

        Args:
            uuid (str): Game uuid
            username (str): username attempting forfeit

        Returns:
            Game: Game forfeited

        Raises:
            InvalidInputException: If username cannot ff at this time,
            or if user not in game
        """

        # Grab game using uuid
        game = self.game_store.get_by_uuid(uuid)

        # Ensure username in game
        if username not in [game.player_one, game.player_two]:
            raise InvalidInputException

        # Can only ff if it is the player's move
        if username == game.player_one and GameState(game.state) != GameState.MOVE_ONE:
            raise InvalidInputException
        if username == game.player_two and GameState(game.state) != GameState.MOVE_TWO:
            raise InvalidInputException

        # ff is valid
        if username == game.player_one:
            game.state = GameState.FF_ONE.value
            game.touch_1()
        if username == game.player_two:
            game.state = GameState.FF_TWO.value
            game.touch_2()
        
        return self.game_store.update_game(game)

    # Poll for update 

# Add game api routes