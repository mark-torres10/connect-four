"""Helper file for gameplay. Manages functions such as setting up the board
using pygame."""
import pygame

import constants as constants
from components import Board


def init_game():
    """Initializes first instance of the game."""
    return pygame.display.set_mode(constants.GAME_SIZE)


def draw_board(board: Board, screen: pygame.Surface):
    """Draws and displays board of current game state using pygame."""

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
            if board[row_num, col_num] == 1:
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
            elif board[row_num, col_num] == 2:
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
