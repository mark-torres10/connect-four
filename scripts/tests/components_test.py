"""Tests for components.

Tested with pytest. Run `pytest` to test."""
import numpy as np

from scripts.constants import COLUMN_COUNT, ROW_COUNT
from scripts.components import Board, Piece


class TestPiece:
    """Tests the 'Piece' class."""

    def test_init_piece(self):
        """Tests init of piece."""
        piece = Piece("red", 1)
        assert piece.color == "red"
        assert piece.value == 1


class TestBoard:
    """Tests the 'Board' class."""

    def __init__(self):
        self.num_rows = ROW_COUNT
        self.num_columns = COLUMN_COUNT

    def test_init_board(self):
        """Tests the 'init_board' method."""
        board = Board(num_rows=self.num_rows, num_columns=self.num_columns)
        assert board.board.shape == (self.num_rows, self.num_columns)
        assert not np.any(board.board)  # test for all zeros
