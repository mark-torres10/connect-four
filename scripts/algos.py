"""Implements NPC opponent algorithms."""
import copy
from random import randint
from typing import Literal

from components import Board
from constants import NUM_IN_A_ROW_TO_WIN

PLAYER_2_VALUE = 2

# maps tuple of player (1 vs. 2) plus how many in a row for that player
# ([0, 4]) to a score. Done from PoV of AI player (P2), so P2 moves have
# positive evaluation and P1 moves have negative evaluation. These values
# can be flipped regardless (since alpha-beta pruning is an optimized minimax)
# algorithm.
ALPHA_BETA_STATE_SCORES = {
    (1, 0): 0,
    (2, 0): 0,
    (1, 1): -1,
    (2, 1): 1,
    (1, 2): -2,
    (2, 2): 2,
    (1, 3): -5,
    (2, 3): 5,
    (1, 4): -100,
    (2, 4): 100
}


def make_move_naive(board: Board):
    """Randomly picks next available move on board."""
    num_cols = board.num_columns
    has_made_next_move = False
    while not has_made_next_move:
        rand_colnum = randint(0, num_cols - 1)
        next_valid_move = board.get_next_valid_row_in_column(
            col_num=rand_colnum
        )
        if next_valid_move is None:
            continue
        else:
            board.drop_piece(col_num=rand_colnum, value=PLAYER_2_VALUE)
            break


def score_game_state(board: Board, player: Literal[1, 2]):
    """Given a certain game state, return score. In the case of an absolute
    value tie, return the score of the current player."""
    max_num_in_a_row_dict = board.get_max_num_in_a_row_dict()
    if len(max_num_in_a_row_dict.keys()) == 0:
        return 0

    max_in_a_row_num = max_num_in_a_row_dict.keys()[0]
    player = max_num_in_a_row_dict[max_in_a_row_num]

    return ALPHA_BETA_STATE_SCORES[(player, max_in_a_row_num)]


def make_move_alpha_beta_pruning(board: Board):
    """Uses alpha-beta pruning to determine next move."""
    dict_next_valid_moves = board.get_dict_next_valid_moves()
    move_tuples_list = []
    for col, row in dict_next_valid_moves.items():
        move_tuples_list.append([row, col])

    # check if any moves can result in an immediate win for you. If so,
    # make that move.
    for (row, col) in move_tuples_list:
        # make deepcopy of board
        test_board = copy.deepcopy(board)
        test_board[row, col] = PLAYER_2_VALUE
        is_game_over, winner = test_board.is_game_over()
        if is_game_over and winner == PLAYER_2_VALUE:
            board[row, col] = PLAYER_2_VALUE

    # assume that AI is doing the max step and that the human player will be
    # doing the min step.

    def _max_value(
        scored_game: int, alpha: int, beta: int,
        is_player_two_turn: bool = True
    ):
        """Perform 'max' step in minimax algorithm."""
        test_board = copy.deepcopy(board)
        value = -999
        dict_next_valid_moves = board.get_dict_next_valid_moves()
        move_tuples_list = []
        for col, row in dict_next_valid_moves.items():
            move_tuples_list.append([row, col])

        for (row, col) in move_tuples_list:
            test_board[row, col] = 2 if is_player_two_turn else 1
            scored_game = score_game_state(test_board)
            value = max(value, _min_value(scored_game, alpha, beta))
            if value >= beta:
                return value
            beta = max(alpha, value)
        return value

    def _min_value(
        scored_game: int, alpha: int, beta: int,
        is_player_two_turn: bool = False
    ):
        """Performs 'min' step in minimax algorithm."""
        test_board = copy.deepcopy(board)
        value = 999
        dict_next_valid_moves = board.get_dict_next_valid_moves()
        move_tuples_list = []
        for col, row in dict_next_valid_moves.items():
            move_tuples_list.append([row, col])

        for (row, col) in move_tuples_list:
            test_board[row, col] = 2 if is_player_two_turn else 1
            scored_game = score_game_state(test_board)
            value = min(value, _max_value(scored_game, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    # implement alpha-beta search
    best_score = -999
    beta = 999
    best_move_row_col = (None, None)

    for (row, col) in move_tuples_list:
        value = _min_value(board, best_score, beta)
        if value > best_score:
            best_score = value
            best_move_row_col = (row, col)

    board[best_move_row_col[0], best_move_row_col[1]] = PLAYER_2_VALUE


def make_move_deep_q_learning(board: Board):
    """Uses deep Q learning in order to make next available move."""
    pass
