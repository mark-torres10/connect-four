"""Components needed to create game."""
from typing import Literal, Tuple

import numpy as np

import scripts.constants as constants


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

    def __init__(
        self,
        num_rows: int = constants.ROW_COUNT,
        num_columns: int = constants.COLUMN_COUNT
    ):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.board = np.zeros((self.num_rows, self.num_columns))
        self.all_possible_diagonals = (
            self._define_all_possible_diagonals_from_all_points()
        )

    def __getitem__(self, row_col_tuple: Tuple[int, int]):
        """Provides dunder so that slicing on the board object automatically
        references the self.board attribute when retrieving items."""
        try:
            iter(row_col_tuple)
        except Exception as e:
            raise ValueError(
                f"Need to pass in a iterable for indexing: {e.__repr__()}"
            )

        row_num, col_num = row_col_tuple

        if not row_num and not col_num:
            return None

        if isinstance(row_num, int) and row_num > self.num_rows - 1:
            return None
        if isinstance(col_num, int) and col_num > self.num_columns - 1:
            return None

        return self.board[row_num, col_num]

    def __setitem__(self, row_col_tuple: Tuple[int, int], new_value):
        """Provides dunder so that slicing on the board object automatically
        references the self.board attribute when setting items.

        Passes in the row and col number as a tuple.
        """
        try:
            iter(row_col_tuple)
        except Exception as e:
            raise ValueError(
                f"Need to pass in a iterable for indexing: {e.__repr__()}"
            )

        if len(row_col_tuple) != 2:
            raise IndexError("Need to specify both a row and column.")

        row_num, col_num = row_col_tuple
        if isinstance(row_num, int) and row_num > self.num_rows - 1:
            return None
        if isinstance(col_num, int) and col_num > self.num_columns - 1:
            return None

        self.board[row_num, col_num] = new_value

    def __repr__(self):
        """Print board state when printing object."""
        return str(self.board)

    def init_board(self):
        """Initialize an empty board."""
        self.board = np.zeros((self.num_rows, self.num_columns))

    # TODO(mark): add test + refactor
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

    def check_is_move_on_board(self, row_num: int, col_num: int):
        """Given a row_num, col_num pair, check if the move is on the board.

        For example, on a N x N board, the move (N + 3, N + 7) wouldn't be in
        the N x N space. Similarly, the move (-3, -3) isn't possible if the
        minimum row and column is 0.

        Returns:
            (bool): True if move is on the board, False otherwise.
        """
        if row_num > self.num_rows - 1:
            return False
        if row_num < 0:
            return False
        if col_num > self.num_columns - 1:
            return False
        if col_num < 0:
            return False

        return True

    def is_valid_move(self, row_num: int, col_num: int):
        """Checks if a given move is valid."""
        if not self.check_is_move_on_board(row_num=row_num, col_num=col_num):
            return False

        if self.board[row_num, col_num] != 0:
            return False

        next_valid_row_in_col = self.get_next_valid_row_in_column(col_num)
        if not next_valid_row_in_col:
            return False
        if row_num != next_valid_row_in_col:
            return False

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
                break

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
                # if 4 values are in a row (and they're not 0),
                # return the value
                if (
                    val_to_player_counter_dict[val]
                    == constants.NUM_IN_A_ROW_TO_WIN
                    and val != 0.0
                ):
                    return val
            else:
                # reset all counters to 0. Update count of most recent value
                for key in val_to_player_counter_dict.keys():
                    val_to_player_counter_dict[key] = 0
                val_to_player_counter_dict[val] += 1

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

    def check_win_connected_in_a_column(self, col_num: int):
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
                # if 4 values are in a column (and they're not 0),
                # return the value
                if (
                    val_to_player_counter_dict[val]
                    == constants.NUM_IN_A_ROW_TO_WIN
                    and val != 0.0
                ):
                    return val
            else:
                # reset all counters to 0. Update count of most recent value
                for key in val_to_player_counter_dict.keys():
                    val_to_player_counter_dict[key] = 0
                val_to_player_counter_dict[val] += 1

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

    def _define_diagonal_from_endpoint(
        self,
        row_num: int,
        col_num: int,
        direction: Literal[
            "upperleft", "upperright", "lowerleft", "lowerright"
        ]
    ):
        """Given an endpoint, defines a diagonal from that endpoint, towards
        a certain direction.

        Returns points as coordinates from left to right.
        """
        if direction not in [
            "upperleft", "upperright", "lowerleft", "lowerright"
        ]:
            print("Please use a valid diagonal direction.")
            return None

        # endpoint is the bottomright most point in the diagonal
        if direction == "upperleft":

            # check if the upperleftmost point of diagonal would be valid
            terminal_row_num = row_num - 3
            terminal_col_num = col_num - 3

            if not self.check_is_move_on_board(
                row_num=terminal_row_num, col_num=terminal_col_num
            ):
                return None

            return np.array([
                np.array([terminal_row_num, terminal_col_num]),
                np.array([terminal_row_num + 1, terminal_col_num + 1]),
                np.array([terminal_row_num + 2, terminal_col_num + 2]),
                np.array([row_num, col_num])
            ])

        # endpoint is in the bottomleft most point in the diagonal
        if direction == "upperright":

            # check if the upperrightmost point of diagonal would be valid.
            terminal_row_num = row_num - 3
            terminal_col_num = col_num + 3

            if not self.check_is_move_on_board(
                row_num=terminal_row_num, col_num=terminal_col_num
            ):
                return None

            return np.array([
                np.array([row_num, col_num]),
                np.array([row_num - 1, col_num + 1]),
                np.array([row_num - 2, col_num + 2]),
                np.array([terminal_row_num, terminal_col_num])
            ])

        # endpoint is in the upperright most point in the diagonal
        if direction == "lowerleft":

            # check if the lowerleftmost point of diagonal would be valid.
            terminal_row_num = row_num + 3
            terminal_col_num = col_num - 3

            if not self.check_is_move_on_board(
                row_num=terminal_row_num, col_num=terminal_col_num
            ):
                return None

            return np.array([
                np.array([terminal_row_num, terminal_col_num]),
                np.array([terminal_row_num - 1, terminal_col_num + 1]),
                np.array([terminal_row_num - 2, terminal_col_num + 2]),
                np.array([row_num, col_num])
            ])

        # endpoint is in the upperleft most point in the diagonal.
        if direction == "lowerright":

            # check if the lowerrightmost point of diagonal would be valid.
            terminal_row_num = row_num + 3
            terminal_col_num = col_num + 3

            if not self.check_is_move_on_board(
                row_num=terminal_row_num, col_num=terminal_col_num
            ):
                return None

            return np.array([
                np.array([row_num, col_num]),
                np.array([row_num + 1, col_num + 1]),
                np.array([row_num + 2, col_num + 2]),
                np.array([terminal_row_num, terminal_col_num])
            ])

        print("No valid direction given for diagonal, returning None.")
        return None

    def _define_all_possible_diagonals_from_point(
        self, row_num: int, col_num: int
    ):
        """Given a point (row_num, col_num) on the board, define all the
        possible diagonals.

        The diagonals, if mapped on top of each other, form an X. The approach
        in this function is to figure out the bounds for that X, then define
        all the diagonals along that X that are 4 units long.

        Maximum amount of diagonals that are 4 units long and involve the
        given point is 6 (if the point is in the middle of the board).
        Minimum number of diagonals is 1 (if the point is on a corner). This
        is true for a 7 x 6 Connect-Four grid. Otherwise, for a larger grid,
        max number of diagonals goes up to 8.

        Returns:
            list_diagonals (List[List[numpy.ndarray]]): list of diagonals,
            where each diagonal is defined by a list of four tuples, typed as
            numpy arrays, indicating the coordinates for that diagonal.
        """
        # get outer bounds for row and column values for diagonals from
        # a given starting point.
        lowest_row_num = row_num - 3
        highest_row_num = row_num + 3
        lowest_col_num = col_num - 3
        highest_col_num = col_num + 3

        # get most valid outer bounds.
        lowest_valid_row_num = max(lowest_row_num, 0)
        highest_valid_row_num = min(highest_row_num, self.num_rows - 1)
        lowest_valid_col_num = max(lowest_col_num, 0)
        highest_valid_col_num = min(highest_col_num, self.num_columns - 1)

        # get outermost coordinates for any possible diagonal.
        upperleft_most_point = np.array(
            [lowest_valid_row_num, lowest_valid_col_num]
        )
        upperright_most_point = np.array(
            [lowest_valid_row_num, highest_valid_col_num]
        )
        lowerleft_most_point = np.array(
            [highest_valid_row_num, lowest_valid_col_num]
        )
        lowerright_most_point = np.array(
            [highest_valid_row_num, highest_valid_col_num]
        )

        # define the two longest possible diagonals (one from top left to
        # bottom right and one from bottom left to top right). Define as pair
        # of tuples from left to right. Along these two diagonals, find
        # all the 4-length subdiagonals.
        list_diagonals = []

        # start first with diagonal from top left to bottom right.
        # going from the upperleft most valid point down to the point in
        # question, define diagonals. Sometimes we might not get a valid
        # diagonal, so this returns None, which we filter later.
        upperleftmost_point_of_possible_diagonal = upperleft_most_point

        while True:
            # if the upperleftmost point is invalid, update the left terminal
            # point to next point in diagonal and continue.

            if not self.check_is_move_on_board(
                row_num=upperleftmost_point_of_possible_diagonal[0],
                col_num=upperleftmost_point_of_possible_diagonal[1]
            ):
                upperleftmost_point_of_possible_diagonal + (1, 1)
                continue

            possible_diagonal = self._define_diagonal_from_endpoint(
                row_num=upperleftmost_point_of_possible_diagonal[0],
                col_num=upperleftmost_point_of_possible_diagonal[1],
                direction="lowerright"
            )

            # verify that original point is in diagonal. This accounts for
            # edge cases on corners where the "diagonal" is actually
            # either a vertical line or a horizontal line.
            if possible_diagonal is not None and any(
                [
                    row_num == coordinate[0] and col_num == coordinate[1]
                    for coordinate in possible_diagonal
                ]
            ):
                list_diagonals.append(possible_diagonal)

            # update left terminal point to next possible point on diagonal.
            upperleftmost_point_of_possible_diagonal += (1, 1)

            # if we've gone past the original point when creating a new
            # diagonal, break.
            if (
                upperleftmost_point_of_possible_diagonal[0] > row_num
                and upperleftmost_point_of_possible_diagonal[1] > col_num
            ):
                break

        # along that same long diagonal, start from the bottom right and go
        # towards the top left.
        lowerrightmost_point_of_possible_diagonal = lowerright_most_point

        while True:
            # if the lowerrightmost point is invalid, update the right
            # terminal point to next point in diagonal and continue.
            if not self.check_is_move_on_board(
                row_num=lowerrightmost_point_of_possible_diagonal[0],
                col_num=lowerrightmost_point_of_possible_diagonal[1]
            ):
                lowerrightmost_point_of_possible_diagonal + (-1, -1)
                continue

            possible_diagonal = self._define_diagonal_from_endpoint(
                row_num=lowerrightmost_point_of_possible_diagonal[0],
                col_num=lowerrightmost_point_of_possible_diagonal[1],
                direction="upperleft"
            )

            # verify that original point is in diagonal. This accounts for
            # edge cases on corners where the "diagonal" is actually
            # either a vertical line or a horizontal line.
            if possible_diagonal is not None and any(
                [
                    row_num == coordinate[0] and col_num == coordinate[1]
                    for coordinate in possible_diagonal
                ]
            ):
                list_diagonals.append(possible_diagonal)

            # update left terminal point to next possible point on diagonal.
            lowerrightmost_point_of_possible_diagonal += (-1, -1)

            # if we've gone past the original point when creating a new
            # diagonal, break.
            if (
                lowerrightmost_point_of_possible_diagonal[0] < row_num
                and lowerrightmost_point_of_possible_diagonal[1] < col_num
            ):
                break

        # continue with the diagonal from bottom left to top right,
        # starting from the lower left side of the diagonal.
        lowerleftmost_point_of_possible_diagonal = lowerleft_most_point

        while True:
            # if the lowerleftmost point is invalid, update the left terminal
            # point to next point in diagonal and continue.
            if not self.check_is_move_on_board(
                row_num=lowerleftmost_point_of_possible_diagonal[0],
                col_num=lowerleftmost_point_of_possible_diagonal[1]
            ):
                lowerleftmost_point_of_possible_diagonal + (-1, 1)
                continue

            possible_diagonal = self._define_diagonal_from_endpoint(
                row_num=lowerleftmost_point_of_possible_diagonal[0],
                col_num=lowerleftmost_point_of_possible_diagonal[1],
                direction="upperright"
            )

            # verify that original point is in diagonal. This accounts for
            # edge cases on corners where the "diagonal" is actually
            # either a vertical line or a horizontal line.
            if possible_diagonal is not None and any(
                [
                    row_num == coordinate[0] and col_num == coordinate[1]
                    for coordinate in possible_diagonal
                ]
            ):
                list_diagonals.append(possible_diagonal)

            # update left terminal point to next possible point on diagonal.
            lowerleftmost_point_of_possible_diagonal += (-1, 1)

            # if we've gone past the original point when creating a new
            # diagonal, break.
            if (
                lowerleftmost_point_of_possible_diagonal[0] < row_num
                and lowerleftmost_point_of_possible_diagonal[1] > col_num
            ):
                break

        # along that same long diagonal, start from the top right and go
        # towards the bottom left.
        upperrightmost_point_of_possible_diagonal = upperright_most_point

        while True:
            # if the upperrightmost point is invalid, update the right
            # terminal point to next point in diagonal and continue.
            if not self.check_is_move_on_board(
                row_num=upperrightmost_point_of_possible_diagonal[0],
                col_num=upperrightmost_point_of_possible_diagonal[1]
            ):
                upperrightmost_point_of_possible_diagonal + (1, -1)
                continue

            possible_diagonal = self._define_diagonal_from_endpoint(
                row_num=upperrightmost_point_of_possible_diagonal[0],
                col_num=upperrightmost_point_of_possible_diagonal[1],
                direction="lowerleft"
            )

            # verify that original point is in diagonal. This accounts for
            # edge cases on corners where the "diagonal" is actually
            # either a vertical line or a horizontal line.
            if possible_diagonal is not None and any(
                [
                    row_num == coordinate[0] and col_num == coordinate[1]
                    for coordinate in possible_diagonal
                ]
            ):
                list_diagonals.append(possible_diagonal)

            # update left terminal point to next possible point on diagonal.
            upperrightmost_point_of_possible_diagonal += (1, -1)

            # if we've gone past the original point when creating a new
            # diagonal, break.
            if (
                upperrightmost_point_of_possible_diagonal[0] > row_num
                and upperrightmost_point_of_possible_diagonal[1] < col_num
            ):
                break

        # get only valid unique coordinates
        list_diagonals_temp = np.array([
            elem for elem in list_diagonals if elem is not None
        ])

        list_diagonals_deduped = np.array(
            np.unique(list_diagonals_temp, axis=0)
        )

        return list_diagonals_deduped

    def _define_all_possible_diagonals_from_all_points(self):
        """Define all possible diagonals across the board.

        Run as part of class instantiation so that the dict of all possible
        diagonals is available as an object attribute.

        Returns:
            dict_point_to_diagonals: Dict[
                Tuple[int, int],
                List[List[numpy.ndarray]]
            ]: dictionary keyed on tuple coordinates that returns as a value
            the list of diagonal coordinates possible from that point (where
            the coordinates are defined as numpy 2-length arrays).
        """
        dict_point_to_diagonals = {}
        for row_num in range(self.num_rows):
            for col_num in range(self.num_columns):
                dict_point_to_diagonals[(row_num, col_num)] = (
                    self._define_all_possible_diagonals_from_point(
                        row_num=row_num, col_num=col_num
                    )
                )

        return dict_point_to_diagonals

    def check_win_connected_in_a_diagonal(self, row_num: int, col_num: int):
        """Checks if there are the required amounts of tokens in a row in a
        any given diagonal from a certain starting point in order to win.

        This requires (1) the list of diagonals possible from a certain point
        and (2) checking the values along the diagonals.

        Each diagonal is a list of four paired tuples.

        Returns:
            winner (int | None): corresponds to Player 1 or Player 2,
            depending on the winner (if any). If no winner, return None
        """
        list_of_diagonals = self.all_possible_diagonals[(row_num, col_num)]

        winner = None
        num_in_a_row = 0

        # see if there's four in a row in any of the diagonals.
        for diagonal in list_of_diagonals:
            for row_num, col_num in diagonal:
                value_at_point = self.board[row_num, col_num]
                if value_at_point == winner:
                    num_in_a_row += 1
                else:
                    num_in_a_row = 0
                    winner = value_at_point
            # if four in a row isn't found, reset and continue.
            # else, return the winning value.
            if num_in_a_row == 4 and winner != 0:
                return winner
            else:
                winner = None
                num_in_a_row = 0

        return None

    def check_win_any_diagonal(self):
        """Check if there's the required connected tokens in any diagonal
        anywhere on the board to win.

        Returns:
            winner (int | None): corresponds to Player 1 or Player 2,
            depending on the winner (if any). If no winner, return None
        """
        for (row_num, col_num) in self.all_possible_diagonals.keys():
            winner = self.check_win_connected_in_a_diagonal(row_num, col_num)
            if winner is not None:
                return winner

        return None

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
