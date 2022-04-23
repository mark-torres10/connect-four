"""Tests for components.

Tested with pytest. Run `pytest` to test."""
import numpy as np
import pytest

from scripts.constants import COLUMN_COUNT, ROW_COUNT
from scripts.components import Board, Piece


@pytest.fixture
def base_board(scope="function"):
    board = Board(num_rows=ROW_COUNT, num_columns=COLUMN_COUNT)
    board.init_board()
    return board


class TestPiece:
    """Tests the 'Piece' class."""

    def test_init_piece(self):
        """Tests init of piece."""
        piece = Piece("red", 1)
        assert piece.color == "red"
        assert piece.value == 1


class TestBoard:
    """Tests the 'Board' class."""

    num_rows = ROW_COUNT
    num_columns = COLUMN_COUNT

    def test_init_board(self):
        """Tests the 'init_board' method."""
        board = Board(num_rows=self.num_rows, num_columns=self.num_columns)
        assert board.board.shape == (self.num_rows, self.num_columns)
        assert not np.any(board.board)  # test for all zeros

    def test_drop_piece(self):
        """Tests the 'drop_piece' method."""
        pass

    def test_is_valid_move(self):
        """Tests the 'is_valid_move' method."""
        pass

    def test_get_next_valid_row_in_column(self, base_board):
        """Tests the 'get_next_valid_row_in_column' method."""
        full_column = np.array([1] * self.num_rows)
        incomplete_column = np.array([1] * (self.num_rows - 1) + [0.0])

        full_column_idx = self.num_columns - 1
        incomplete_column_idx = self.num_columns - 2

        base_board[:, full_column_idx] = full_column
        base_board[:, full_column_idx]
        base_board[:, incomplete_column_idx] = incomplete_column

        assert base_board.get_next_valid_row_in_column(full_column_idx) is None
        assert (
            base_board.get_next_valid_row_in_column(incomplete_column_idx)
            == (self.num_rows - 1)  # last slot should be free
        )

    def test_check_if_any_valid_moves(self, base_board):
        """Tests the 'check_if_any_valid_moves' method."""
        # an empty board should have valid moves.
        assert base_board.check_if_any_valid_moves()

        full_board = Board(
            num_rows=self.num_rows, num_columns=self.num_columns
        )

        # a full board should not have valid moves
        full_board.board = np.random.rand(self.num_rows, self.num_columns)
        assert not full_board.check_if_any_valid_moves()

        # a partially empty board should have valid moves. Make some slots
        # empty and check that the board now has valid moves.
        full_board[(1, 1)] = 0.0
        full_board[(2, 2)] = 0.0

        assert full_board.check_if_any_valid_moves()

    def test_check_win_connected_in_a_row(self, base_board):
        pass
