from enum import Enum
from typing import List, Optional
import flask
import uuid
from datetime import datetime
from flaskapp.routes.api.user import UserStore
from helpers import SUPPORTED_GAMES, InvalidInputException
from ..__init__ import app 

GAME_TIMEOUT = 120
    
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
    def check_end(board_string: str) -> GameState:
        """
        Check for game end

        Args:
            board_string (str): Current board state

        Returns:
            GameState: Appropriate state (excludes forfeits and timeouts)
        """

        NROW = 6;
        NCOL = 7;

        # Make board in row major format
        board = [[0]*NCOL for _ in range(NROW)]
        
        # Update board from string
        # 1 is p1: 2 is p2
        for i,c in enumerate(board_string):
            # c is 0-based column num
            # Find next available row in column
            next_available_row = -1
            for r in range(NROW):
                if board[r][c] != 0:
                    next_available_row = r
                    break
            assert(next_available_row >= 0)
            
            # Place token
            board[next_available_row, c] = 1 if i % 2 == 0 else 2
        
        # Check for win
        # Horz (right) check
        for i in range(NROW):
            for j in range(NCOL - 3):
                if board[i][j] != 0:
                    to_win = board[i][j]
                    for d in range(1,4):
                        if board[i][j+d] != to_win:
                            # No win




        # Vert check

        # UR

        # DR check




        # No win; check for draw
        if len(board_string) >= 6*7:
            return GameState.DRAW

        # No end; get next player
        if (len(board_string)%2):
            return GameState.MOVE_ONE
        else:
            return GameState.MOVE_TWO


# Game model

    




# Add game api routes