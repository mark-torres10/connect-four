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

    def init_board(self):
        """Initialize an empty board."""
        self.board = np.zeros((self.num_rows, self.num_columns))

    def drop_piece(self, col_num: int, piece: Piece):
        """Drops a piece onto the board.

        Players can only choose the column that they drop a piece into, so we
        limit the input to only be column + the piece that the player uses.
        """
        if not self.is_valid_move(col_num=col_num):
            print("A piece can't be moved there.")
            return

        next_valid_row_num = self.get_next_valid_row_in_column(col_num)
        if not next_valid_row_num:
            print("A piece can't be moved there.")
            return

        self.board[[next_valid_row_num, col_num]] = piece.value

    def is_valid_move(self, row_num, col_num):
        """Checks if a given move is valid."""
        # TODO(mark): see if move is within board
        # TODO(mark): see if a piece is already in that space
        # TODO(mark): see if a new piece can move to the space
        return True

    def get_next_valid_row_in_column(self, col_num: int):
        """Gets the next valid row number available in a column.

        A row is valid if it doesn't already have a number in it
        (e.g., 1 or 2), but instead has 0.0.

        If no valid row, return None.
        """
        column = self.board[:, col_num]

        row_num = None

        for i in range(column.size):
            if column[i] == 0:
                row_num = i

        return row_num

    def check_if_any_valid_moves(self):
        """Checks if any valid moves can still be made on the board.

        Checks if there are any empty spots in the board.
        """
        return 0 in self.board

    def check_win_connected_in_a_row(self, row_num: int):
        """Checks if there are the required amounts of tokens in a row in
        a given row in order to win.

        Returns:
            winner (int | None): corresponds to Player 1 or Player 2,
            depending on the winner (if any). If no winner, return None
        """
        # 0.0 = nobody is there, 1 = player 1, 2 = player 2
        val_to_player_counter_dict = {
            0: 0,
            1: 0,
            2: 0
        }

        first_value = self.board[row_num, 0]
        last_val_seen = first_value
        val_to_player_counter_dict[last_val_seen] += 1

        row = self.board[row_num, :]

        # start comparisons at second value
        for val in row[1:]:
            if val not in [0, 1, 2]:
                continue
            # update counter if current value == previous value
            if val == last_val_seen:
                val_to_player_counter_dict[val] += 1
                if (
                    val_to_player_counter_dict[val]
                    == constants.NUM_IN_A_ROW_TO_WIN
                ):
                    return val
            else:
                # reset all counters to 0.
                for key in val_to_player_counter_dict.keys():
                    val_to_player_counter_dict[key] = 0

            # set last seen value to current first_value
            last_val_seen = val

        # no matches -> return None
        return None

    def check_win_any_row(self):
        """Check if there's the required connected tokens in any row to win.

        Returns:
            winner (int | None): corresponds to Player 1 or Player 2,
            depending on the winner (if any). If no winner, return None
        """
        row_winners = [
            self.check_win_connected_in_a_row(row_num)
            for row_num in range(self.num_rows)
        ]

        if any(row_winners):
            # assumes that there's only one instance where a row can be a
            # winner and that multiple rows can't simultaneously all
            # be winners.
            for val in row_winners:
                if val is not None:
                    return val
        else:
            return None

    def check_win_connected_in_a_column(self, col_num):
        """Checks if there are the required amounts of tokens in a row in
        a given column in order to win.

        Returns:
            winner (int | None): corresponds to Player 1 or Player 2,
            depending on the winner (if any). If no winner, return None
        """
        # 0.0 = nobody is there, 1 = player 1, 2 = player 2
        val_to_player_counter_dict = {
            0: 0,
            1: 0,
            2: 0
        }

        first_value = self.board[0, col_num]
        last_val_seen = first_value
        val_to_player_counter_dict[last_val_seen] += 1

        column = self.board[:, col_num]

        # start comparisons at second value
        for val in column[1:]:
            if val not in [0, 1, 2]:
                continue
            # update counter if current value == previous value
            if val == last_val_seen:
                val_to_player_counter_dict[val] += 1
                if (
                    val_to_player_counter_dict[val]
                    == constants.NUM_IN_A_ROW_TO_WIN
                ):
                    return val
            else:
                # reset all counters to 0.
                for key in val_to_player_counter_dict.keys():
                    val_to_player_counter_dict[key] = 0

            # set last seen value to current first_value
            last_val_seen = val

        # no matches -> return None
        return None

    def check_win_any_column(self):
        """Check if there's the required connected tokens in any column
        to win.

        Returns:
            winner (int | None): corresponds to Player 1 or Player 2,
            depending on the winner (if any). If no winner, return None
        """
        column_winners = [
            self.check_win_connected_in_a_column(col_num)
            for col_num in range(self.num_columns)
        ]

        if any(column_winners):
            # assumes that there's only one instance where a column can be a
            # winner and that multiple columns can't simultaneously all
            # be winners.
            for val in column_winners:
                if val is not None:
                    return val
        else:
            return None

    # TODO(mark): define diagonal checker
    def check_win_connected_in_a_diagonal(self, row_num: int, col_num: int):
        """Checks if there are the required amounts of tokens in a row in a
        given diagonal in order to win.

        Returns:
            winner (int | None): corresponds to Player 1 or Player 2,
            depending on the winner (if any). If no winner, return None
        """
        pass

    def check_win_any_diagonal(self):
        """Check if there's the required connected tokens in any diagonal
        to win.

        Returns:
            winner (int | None): corresponds to Player 1 or Player 2,
            depending on the winner (if any). If no winner, return None
        """
        pass

    def is_game_over(self):
        """Checks to see if the game is over.

        Returns:
            has_winner (bool): is the game over?
            winner (int): corresponds to Player 1 or Player 2, depending on
            the winner.
        """
        # check if there is a winner

        row_winner = self.check_win_any_row()
        column_winner = self.check_win_any_column()
        diagonal_winner = self.check_win_any_diagonal()

        has_winner = any([row_winner, column_winner, diagonal_winner])

        winner = None

        if has_winner:
            for elem in [row_winner, column_winner, diagonal_winner]:
                if elem is not None:
                    winner = elem

        if has_winner and winner:
            return True, winner

        # if there is no winner, check if the game is over or if additional
        # moves can still be made. Also return None since neither player has
        # won.
        return self.check_if_any_valid_moves(), None
