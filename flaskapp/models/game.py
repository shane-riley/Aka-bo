from datetime import datetime, timezone
from enum import Enum
import uuid

from flaskapp.shared import *
from .model import Model

class GameSquare(Enum):
    """
    GameSquare Enum

    One of three states (0-based for clarity)
    """
    EMPTY = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2

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

class Game(Model):
    """
    Generic class for games
    NOTE: only two-player games at the moment
    """

    KIND = 'Game'

    def __init__(self,
                 created=datetime.now(tz=timezone.utc),
                 player_one="",
                 player_two="",
                 board="",
                 state=GameState.MOVE_ONE.value):
        """
        Creates a game

        # NOTE: This is fixed as C4 for now

        Args:
            created (float, optional): Time of creation. Defaults to datetime.now().timestamp().
            player_one (str, optional): Player one username. Defaults to "".
            player_two (str, optional): Player two username. Defaults to "".
            board (Board, optional): Board layout as string. Defaults to "".
            state (GameState, optional): State of game. Defaults to GameState.MOVE_ONE.value.
        """
        self.uuid = str(uuid.uuid4())
        self.created = created
        self.player_one = player_one
        self.player_two = player_two
        self.board=board
        self.state=state
        self.player_one_polled = created
        self.player_two_polled = created
        self.player_one_expires = created + GAME_TIMEOUT
        self.player_two_expires = created + GAME_TIMEOUT


    # Check move legal
    def is_legal(self, move: int) -> bool:
        """
        Check move legality

        Args:
            move (int): column to drop

        Returns:
            bool: whether move is legal
        """

        # Ensure move in 0-based range
        if move < 0 or move >= NCOL:
            return False
        
        # Else

        # Ensure move is not in full column
        return not self.board.count(str(move)) >= NROW

    # Apply move
    def apply_move(self, move: int):
        """
        Apply a move

        If not legal, throw IllegalMoveException

        Args:
            move (int): Column to drop
        """

        if self.is_legal(move):
            # Add the move to the board
            self.board = self.board + str(move)
            self.update_state()
        else:
            raise IllegalMoveException

    # Update state from board
    def update_state(self):
        """
        Update state from board
        """
        # Make 2D array (row major)
        board_arr = [[GameSquare.EMPTY]*NCOL for _ in range(NROW)]

        # Load board into array
        for i,move in enumerate(self.board):
            # Make int
            move = int(move)
            # Players alternate turns
            token = GameSquare.PLAYER_ONE if i % 2 == 0 else GameSquare.PLAYER_TWO

            # Find row to place
            r_to_place = -1
            for r in range(NROW):
                if board_arr[r][move] == GameSquare.EMPTY:
                    r_to_place = r
                    break
            assert(r_to_place > -1)

            # Place piece
            board_arr[r_to_place][move] = token
        
        # Board loaded; check for win
        
        # Horz win (going to right)
        for r in range(NROW):
            for c in range(NCOL-NCONNECT):
                # (r,c) is starting index
                token = board_arr[r][c]
                if token == GameSquare.EMPTY: continue
                # Check whether all match
                won = True
                for d in range(1, NCONNECT):
                    if token != board_arr[r][c+d]:
                        won = False
                        break
                if won:
                    self.state = GameState.WIN_ONE.value if token == GameSquare.PLAYER_ONE else GameState.WIN_TWO.value
                    return self.state
        
        # Vert win (going up)
        for r in range(NROW-NCONNECT):
            for c in range(NCOL):
                # (r,c) is starting index
                token = board_arr[r][c]
                if token == GameSquare.EMPTY: continue
                # Check whether all match
                won = True
                for d in range(1, NCONNECT):
                    if token != board_arr[r+d][c]:
                        won = False
                        break
                if won:
                    self.state = GameState.WIN_ONE.value if token == GameSquare.PLAYER_ONE else GameState.WIN_TWO.value
                    return self.state

        # Diag win (going up and right)
        for r in range(NROW-NCONNECT):
            for c in range(NCOL-NCONNECT):
                # (r,c) is starting index
                token = board_arr[r][c]
                if token == GameSquare.EMPTY: continue
                # Check whether all match
                won = True
                for d in range(1, NCONNECT):
                    if token != board_arr[r+d][c+d]:
                        won = False
                        break
                if won:
                    self.state = GameState.WIN_ONE.value if token == GameSquare.PLAYER_ONE else GameState.WIN_TWO.value
                    return self.state

        # Diag win (going down and right)
        for r in range(NCONNECT-1, NROW):
            for c in range(NCOL-NCONNECT):
                # (r,c) is starting index
                token = board_arr[r][c]
                if token == GameSquare.EMPTY: continue
                # Check whether all match
                won = True
                for d in range(1, NCONNECT):
                    if token != board_arr[r-d][c+d]:
                        won = False
                        break
                if won:
                    self.state = GameState.WIN_ONE.value if token == GameSquare.PLAYER_ONE else GameState.WIN_TWO.value
                    return self.state

        # Check for draw
        if len(self.board) >= NCOL*NROW:
            self.state = GameState.DRAW.value
            return self.state

        # No draw; get next player
        if (len(self.board) % 2):
            self.state = GameState.MOVE_TWO.value
        else:
            self.state = GameState.MOVE_ONE.value
        return self.state

    # Update methods
    def touch_1(self):
        """
        Updates Player 1
        """
        n = datetime.now(tz=timezone.utc)
        self.player_one_polled = n
        self.player_one_expires = n + GAME_TIMEOUT

    def touch_2(self):
        """
        Updates Player 2
        """
        n = datetime.now(tz=timezone.utc)
        self.player_two_polled = n
        self.player_two_expires = n + GAME_TIMEOUT

    def complete(self) -> bool:
        """
        Return true iff game is over

        Returns:
            bool: Game is over
        """
        return GameState(self.state) not in [GameState.MOVE_ONE, GameState.MOVE_TWO]