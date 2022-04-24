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

    def test_check_is_move_on_board(self, base_board):
        """Tests the 'check_is_move_on_board' method."""
        assert not base_board.check_is_move_on_board(row_num=100, col_num=0)
        assert not base_board.check_is_move_on_board(row_num=-100, col_num=0)
        assert not base_board.check_is_move_on_board(row_num=0, col_num=100)
        assert not base_board.check_is_move_on_board(row_num=0, col_num=-100)
        assert base_board.check_is_move_on_board(row_num=1, col_num=1)

    def test_is_valid_move(self, base_board):
        """Tests the 'is_valid_move' method."""
        # test 1: move would be onto a space not on the board
        assert not base_board.is_valid_move(row_num=100, col_num=0)

        # test 2: there is already a nonzero value on that space
        base_board[1, 1] = 1
        assert not base_board.is_valid_move(row_num=1, col_num=1)

        # test 3: the move is onto a square whose row isn't the next available
        # row in a column
        base_board[0, 3] = 1
        assert not base_board.is_valid_move(row_num=3, col_num=3)

        # test 4: the move is onto a valid empty square that is the next
        # available spot (given that [0, 3] is now occupied)
        assert base_board.is_valid_move(row_num=1, col_num=3)

    def test_get_next_valid_row_in_column(self, base_board):
        """Tests the 'get_next_valid_row_in_column' method."""
        full_column = np.array([1] * self.num_rows)
        incomplete_column = np.array([1] * (self.num_rows - 1) + [0.0])

        full_column_idx = self.num_columns - 1
        incomplete_column_idx = self.num_columns - 2

        base_board[:, full_column_idx] = full_column
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
        """Tests the 'check_win_connected_in_a_row' method."""
        empty_row = np.zeros(self.num_columns)
        no_connect_four_row = np.array([1, 2, 0, 1, 2, 0])
        connect_four_beginning_of_row = np.array([1, 1, 1, 1, 0, 2])
        connect_four_middle_of_row = np.array([1, 2, 2, 2, 2, 1])
        connect_four_end_of_row = np.array([1, 0, 2, 2, 2, 2])

        base_board[0, :] = empty_row
        base_board[1, :] = no_connect_four_row
        base_board[2, :] = connect_four_beginning_of_row
        base_board[3, :] = connect_four_middle_of_row
        base_board[4, :] = connect_four_end_of_row

        assert base_board.check_win_connected_in_a_row(0) is None
        assert base_board.check_win_connected_in_a_row(1) is None
        assert base_board.check_win_connected_in_a_row(2) == 1
        assert base_board.check_win_connected_in_a_row(3) == 2
        assert base_board.check_win_connected_in_a_row(4) == 2

    def test_check_win_any_row(self, base_board):
        """Tests the 'check_win_any_row' method."""
        # base board, with all zeros, should have None
        assert base_board.check_win_any_row() is None

        # board with one row that wins for Player 2
        new_board = Board()
        new_board.init_board()
        connect_four_middle_of_row = np.array([1, 2, 2, 2, 2, 1])
        new_board[1, :] = connect_four_middle_of_row
        assert new_board.check_win_any_row() == 2

    def test_check_win_connected_in_a_column(self, base_board):
        """Tests the 'check_win_connected_in_a_column' method."""
        empty_column = np.zeros(self.num_rows)
        no_connect_four_column = np.array([1, 2, 0, 1, 2, 0, 1])
        connect_four_beginning_of_column = np.array([1, 1, 1, 1, 0, 2, 0])
        connect_four_middle_of_column = np.array([1, 2, 2, 2, 2, 1, 1])
        connect_four_end_of_column = np.array([1, 0, 0, 2, 2, 2, 2])

        base_board[:, 0] = empty_column
        base_board[:, 1] = no_connect_four_column
        base_board[:, 2] = connect_four_beginning_of_column
        base_board[:, 3] = connect_four_middle_of_column
        base_board[:, 4] = connect_four_end_of_column

        assert base_board.check_win_connected_in_a_column(0) is None
        assert base_board.check_win_connected_in_a_column(1) is None
        assert base_board.check_win_connected_in_a_column(2) == 1
        assert base_board.check_win_connected_in_a_column(3) == 2
        assert base_board.check_win_connected_in_a_column(4) == 2

    def test_check_win_any_column(self, base_board):
        """Tests the 'check_win_any_column' method."""
        # base board, with all zeros, should have None
        assert base_board.check_win_any_column() is None

        # board with one column that wins for Player 2
        new_board = Board()
        new_board.init_board()
        connect_four_middle_of_column = np.array([1, 2, 2, 2, 2, 1, 1])
        new_board[:, 1] = connect_four_middle_of_column
        assert new_board.check_win_any_column() == 2

    def test_define_diagonal_from_endpoint(self, base_board):
        """Tests the '_define_diagonal_from_endpoint' method."""
        directions = ["upperleft", "upperright", "lowerleft", "lowerright"]

        # test 1: coordinate is in the top left corner. Only "lowerright"
        # should give results.
        list_of_possible_diagonals = [
            base_board._define_diagonal_from_endpoint(
                row_num=0, col_num=0, direction=direction
            )
            for direction in directions
        ]

        assert list_of_possible_diagonals[0] is None
        assert list_of_possible_diagonals[1] is None
        assert list_of_possible_diagonals[2] is None
        assert np.array_equal(
            list_of_possible_diagonals[3],
            np.array([
                np.array([0, 0]), np.array([1, 1]),
                np.array([2, 2]), np.array([3, 3])
            ])
        )

        # test 2: coordinate is in the middle of the top row. Only "lowerleft"
        # should give results. Shifting col_num to 2 instead of 3 would mean
        # only "lowerright" would give results.
        list_of_possible_diagonals = [
            base_board._define_diagonal_from_endpoint(
                row_num=0, col_num=3, direction=direction
            )
            for direction in directions
        ]
        assert list_of_possible_diagonals[0] is None
        assert list_of_possible_diagonals[1] is None
        assert np.array_equal(
            list_of_possible_diagonals[2],
            np.array([
                np.array([3, 0]), np.array([2, 1]),
                np.array([1, 2]), np.array([0, 3])
            ])
        )
        assert list_of_possible_diagonals[3] is None

        # test 3: coordinate is in the top right corner. Only "lowerleft"
        # should give results.
        list_of_possible_diagonals = [
            base_board._define_diagonal_from_endpoint(
                row_num=0, col_num=5, direction=direction
            )
            for direction in directions
        ]
        assert list_of_possible_diagonals[0] is None
        assert list_of_possible_diagonals[1] is None
        assert np.array_equal(
            list_of_possible_diagonals[2],
            np.array([
                np.array([3, 2]), np.array([2, 3]),
                np.array([1, 4]), np.array([0, 5])
            ])
        )
        assert list_of_possible_diagonals[3] is None

        # test 4: coordinate is in the middle row of the last column. Both
        # "upperleft" and "lowerleft" should give results.
        list_of_possible_diagonals = [
            base_board._define_diagonal_from_endpoint(
                row_num=3, col_num=5, direction=direction
            )
            for direction in directions
        ]
        assert np.array_equal(
            list_of_possible_diagonals[0],
            np.array([
                np.array([0, 2]), np.array([1, 3]),
                np.array([2, 4]), np.array([3, 5])
            ])
        )
        assert list_of_possible_diagonals[1] is None
        assert np.array_equal(
            list_of_possible_diagonals[2],
            np.array([
                np.array([6, 2]), np.array([5, 3]),
                np.array([4, 4]), np.array([3, 5])
            ])
        )
        assert list_of_possible_diagonals[3] is None

        # test 5: coordinate is in the bottom right corner. Only "upperleft"
        # should give results.
        list_of_possible_diagonals = [
            base_board._define_diagonal_from_endpoint(
                row_num=6, col_num=5, direction=direction
            )
            for direction in directions
        ]

        assert np.array_equal(
            list_of_possible_diagonals[0],
            np.array([
                np.array([3, 2]), np.array([4, 3]),
                np.array([5, 4]), np.array([6, 5])
            ])
        )
        assert list_of_possible_diagonals[1] is None
        assert list_of_possible_diagonals[2] is None
        assert list_of_possible_diagonals[3] is None

        # test 6: coordinate is in the middle of the bottom row. Only
        # "upperright" will give results. Shifting col_num from 2 to 3
        # will mean that "upperleft" would give results.
        list_of_possible_diagonals = [
            base_board._define_diagonal_from_endpoint(
                row_num=6, col_num=2, direction=direction
            )
            for direction in directions
        ]

        assert list_of_possible_diagonals[0] is None
        assert np.array_equal(
            list_of_possible_diagonals[1],
            np.array([
                np.array([6, 2]), np.array([5, 3]),
                np.array([4, 4]), np.array([3, 5])
            ])
        )
        assert list_of_possible_diagonals[2] is None
        assert list_of_possible_diagonals[3] is None

        # test 7: coordinate is in the bottom left corner. Only "upperright"
        # should give results.
        list_of_possible_diagonals = [
            base_board._define_diagonal_from_endpoint(
                row_num=6, col_num=0, direction=direction
            )
            for direction in directions
        ]

        assert list_of_possible_diagonals[0] is None
        assert np.array_equal(
            list_of_possible_diagonals[1],
            np.array([
                np.array([6, 0]), np.array([5, 1]),
                np.array([4, 2]), np.array([3, 3])
            ])
        )
        assert list_of_possible_diagonals[2] is None
        assert list_of_possible_diagonals[3] is None

        # test 8: coordinate is in the middle row of the first column. Both
        # "upperright" and "lowerright" should give results.
        list_of_possible_diagonals = [
            base_board._define_diagonal_from_endpoint(
                row_num=3, col_num=0, direction=direction
            )
            for direction in directions
        ]
        assert list_of_possible_diagonals[0] is None
        assert np.array_equal(
            list_of_possible_diagonals[1],
            np.array([
                np.array([3, 0]), np.array([2, 1]),
                np.array([1, 2]), np.array([0, 3])
            ])
        )
        assert list_of_possible_diagonals[2] is None
        assert np.array_equal(
            list_of_possible_diagonals[3],
            np.array([
                np.array([3, 0]), np.array([4, 1]),
                np.array([5, 2]), np.array([6, 3])
            ])
        )
        # test 9: coordinate is right in the middle of the board. In this
        # example, only "lowerleft" and "upperleft" should give results.
        list_of_possible_diagonals = [
            base_board._define_diagonal_from_endpoint(
                row_num=3, col_num=3, direction=direction
            )
            for direction in directions
        ]
        assert np.array_equal(
            list_of_possible_diagonals[0],
            np.array([
                np.array([0, 0]), np.array([1, 1]),
                np.array([2, 2]), np.array([3, 3])
            ])
        )
        assert list_of_possible_diagonals[1] is None
        assert np.array_equal(
            list_of_possible_diagonals[2],
            np.array([
                np.array([6, 0]), np.array([5, 1]),
                np.array([4, 2]), np.array([3, 3])
            ])
        )
        assert list_of_possible_diagonals[3] is None

    def test_define_all_possible_diagonals_from_point(self, base_board):
        """Tests the '_define_all_possible_diagonals_from_point' method."""

        # test 1: coordinate is in the top left corner. Should only be one
        # possible diagonal.
        list_diagonals = base_board._define_all_possible_diagonals_from_point(
            row_num=0, col_num=0
        )
        assert len(list_diagonals) == 1
        assert np.array_equal(
            list_diagonals,
            np.array([[
                np.array([0, 0]),
                np.array([1, 1]),
                np.array([2, 2]),
                np.array([3, 3]),
            ]])
        )

        # test 2: coordinate is in the middle of the top row.
        list_diagonals = base_board._define_all_possible_diagonals_from_point(
            row_num=0, col_num=3
        )
        assert len(list_diagonals) == 1
        assert np.array_equal(
            list_diagonals,
            np.array([[
                np.array([3, 0]),
                np.array([2, 1]),
                np.array([1, 2]),
                np.array([0, 3]),
            ]])
        )

        # test 3: coordinate is in the top right corner.
        list_diagonals = base_board._define_all_possible_diagonals_from_point(
            row_num=0, col_num=5
        )
        assert len(list_diagonals) == 1
        assert np.array_equal(
            list_diagonals,
            np.array([[
                np.array([3, 2]),
                np.array([2, 3]),
                np.array([1, 4]),
                np.array([0, 5]),
            ]])
        )

        # test 4: coordinate is in the middle row of the last column.
        list_diagonals = base_board._define_all_possible_diagonals_from_point(
            row_num=3, col_num=5
        )
        assert len(list_diagonals) == 2
        assert np.array_equal(
            list_diagonals,
            np.array([
                [
                    np.array([0, 2]),
                    np.array([1, 3]),
                    np.array([2, 4]),
                    np.array([3, 5]),
                ],
                [
                    np.array([6, 2]),
                    np.array([5, 3]),
                    np.array([4, 4]),
                    np.array([3, 5]),
                ]
            ])
        )

        # test 5: coordinate is in the bottom right corner.
        list_diagonals = base_board._define_all_possible_diagonals_from_point(
            row_num=6, col_num=5
        )
        assert len(list_diagonals) == 1
        assert np.array_equal(
            list_diagonals,
            np.array([[
                np.array([3, 2]),
                np.array([4, 3]),
                np.array([5, 4]),
                np.array([6, 5]),
            ]])
        )

        # test 6: coordinate is in the middle of the bottom row.
        list_diagonals = base_board._define_all_possible_diagonals_from_point(
            row_num=6, col_num=2
        )
        assert len(list_diagonals) == 1
        assert np.array_equal(
            list_diagonals,
            np.array([[
                np.array([6, 2]),
                np.array([5, 3]),
                np.array([4, 4]),
                np.array([3, 5]),
            ]])
        )

        # test 7: coordinate is in the bottom left corner.
        list_diagonals = base_board._define_all_possible_diagonals_from_point(
            row_num=6, col_num=0
        )
        assert len(list_diagonals) == 1
        assert np.array_equal(
            list_diagonals,
            np.array([[
                np.array([6, 0]),
                np.array([5, 1]),
                np.array([4, 2]),
                np.array([3, 3]),
            ]])
        )

        # test 8: coordinate is in the middle row of the first column.
        list_diagonals = base_board._define_all_possible_diagonals_from_point(
            row_num=3, col_num=0
        )
        assert len(list_diagonals) == 2
        assert np.array_equal(
            list_diagonals,
            np.array([
                [
                    np.array([3, 0]),
                    np.array([2, 1]),
                    np.array([1, 2]),
                    np.array([0, 3]),
                ],
                [
                    np.array([3, 0]),
                    np.array([4, 1]),
                    np.array([5, 2]),
                    np.array([6, 3]),
                ]
            ])
        )

        # test 9: coordinate is right in the middle of the board.
        list_diagonals = base_board._define_all_possible_diagonals_from_point(
            row_num=3, col_num=3
        )
        assert len(list_diagonals) == 6
        assert np.array_equal(
            list_diagonals,
            np.array([
                [
                    np.array([0, 0]),
                    np.array([1, 1]),
                    np.array([2, 2]),
                    np.array([3, 3]),
                ],
                [
                    np.array([1, 1]),
                    np.array([2, 2]),
                    np.array([3, 3]),
                    np.array([4, 4]),
                ],
                [
                    np.array([2, 2]),
                    np.array([3, 3]),
                    np.array([4, 4]),
                    np.array([5, 5]),
                ],
                [
                    np.array([4, 2]),
                    np.array([3, 3]),
                    np.array([2, 4]),
                    np.array([1, 5]),
                ],
                [
                    np.array([5, 1]),
                    np.array([4, 2]),
                    np.array([3, 3]),
                    np.array([2, 4]),
                ],
                [
                    np.array([6, 0]),
                    np.array([5, 1]),
                    np.array([4, 2]),
                    np.array([3, 3]),
                ],
            ])
        )
