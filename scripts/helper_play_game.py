"""Helper file for gameplay. Manages functions such as setting up the board
using pygame."""
import copy
from typing import Literal

import numpy as np
import pygame

from algos import (
    make_move_alpha_beta_pruning, make_move_deep_q_learning, make_move_naive
)
import constants as constants
from components import Board

COMPUTER_OPPONENT_TO_ALGO = {
    "easy": make_move_naive,
    "medium": make_move_alpha_beta_pruning,
    "hard": make_move_deep_q_learning
}


def init_game():
    """Initializes first instance of the game."""
    return pygame.display.set_mode(constants.GAME_SIZE)


def draw_board(board: Board, screen: pygame.Surface):
    """Draws and displays board of current game state using pygame."""

    # flip board to correctly display pieces (upside down)
    # TODO(mark): find cleaner implementation. We want the display to go
    # from bottom to top, but board implementation is easiest from top to
    # bottom (since 0th row is first row). As temporary workaround, currently
    # just flipping the board.
    new_board = copy.deepcopy(board)
    new_board.board = np.flip(new_board.board, axis=0)

    # draw Connect Four slots
    for col_num in range(constants.COLUMN_COUNT):
        for row_num in range(constants.ROW_COUNT):
            pygame.draw.rect(
                screen,
                constants.COLOR_TO_CODE_DICT["blue"],
                (
                    (col_num * constants.SQUARESIZE) + constants.SQUARESIZE,
                    (row_num * constants.SQUARESIZE) + constants.SQUARESIZE,
                    constants.SQUARESIZE,
                    constants.SQUARESIZE
                )
            )
            pygame.draw.circle(
                screen,
                constants.COLOR_TO_CODE_DICT["black"],
                (
                    int(
                        ((col_num + 1) * constants.SQUARESIZE)
                        + (constants.SQUARESIZE / 2)
                    ),
                    int(
                        ((row_num + 1) * constants.SQUARESIZE)
                        + (constants.SQUARESIZE / 2)
                    ),
                ),
                constants.SLOT_RADIUS
            )

    # draw pieces on the board
    for col_num in range(constants.COLUMN_COUNT):
        for row_num in range(constants.ROW_COUNT):
            # draw Player 1's pieces:
            if new_board[row_num, col_num] == 1:
                pygame.draw.circle(
                    screen,
                    constants.COLOR_TO_CODE_DICT[
                        constants.VALUE_TO_COLOR_DICT[1]
                    ],
                    (
                        int(
                            ((col_num + 1) * constants.SQUARESIZE)
                            + (constants.SQUARESIZE / 2)
                        ),
                        int(
                            ((row_num + 1) * constants.SQUARESIZE)
                            + (constants.SQUARESIZE / 2)
                        ),
                    ),
                    constants.SLOT_RADIUS
                )
            # draw Player 2's pieces:
            elif new_board[row_num, col_num] == 2:
                pygame.draw.circle(
                    screen,
                    constants.COLOR_TO_CODE_DICT[
                        constants.VALUE_TO_COLOR_DICT[2]
                    ],
                    (
                        int(
                            ((col_num + 1) * constants.SQUARESIZE)
                            + (constants.SQUARESIZE / 2)
                        ),
                        int(
                            ((row_num + 1) * constants.SQUARESIZE)
                            + (constants.SQUARESIZE / 2)
                        ),
                    ),
                    constants.SLOT_RADIUS
                )

    # update display
    pygame.display.update()


def computer_make_move(
    board: Board, difficulty_level: Literal["easy", "medium", "hard"]
):
    """Computer opponent makes a move.

    Wrapper function around the actual function that makes the move and updates
    the board.
    """
    func = COMPUTER_OPPONENT_TO_ALGO[difficulty_level]
    func(board)
