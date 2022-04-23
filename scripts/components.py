"""Components needed to create game."""
from typing import Literal

import numpy as np

import constants

class Piece:
    """Used to define the pieces that each player uses.
    
    Each player will use a separate instance, initialized with a color
    and a value mapped to their piece (either a 1 or 2, depending on if they
    are Player 1 or Player 2).
    """
    def __init__(self, color: str, value: Literal[1, 2]):
        self.color = color
        self.value = value


class Board:
    """Used to define the board that the players are playing on."""
    
    def __init__(self):
        self.num_rows = constants.ROW_COUNT
        self.num_columns = constants.COLUMN_COUNT
        self.board = np.zeros((self.num_rows, self.num_columns))
    
    def drop_piece(self, row_num: int, col_num: int, piece: Piece):
        """Drops a piece onto the board."""
        if not self.is_valid_move(row_num=row_num, col_num=col_num):
            return
        
        self.board[[row_num, col_num]] = piece.value

    def is_valid_move(self, row_num, col_num):
        """Checks if a given move is valid."""
        # TODO(mark): see if move is within board
        # TODO(mark): see if a piece is already in that space
        # TODO(mark): see if a new piece can move to the space
        return True

    def check_is_game_over(self):
        """Checks to see if the game is over."""
        pass
