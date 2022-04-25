"""Helper file for gameplay. Manages functions such as setting up the board
using pygame."""
import pygame

import scripts.constants as constants
from scripts.components import Board, Piece


def init_game():
    """Initializes first instance of the game."""
    return pygame.display.set_mode(constants.GAME_SIZE)

def draw_board(board: Board, screen: pygame.Display):
    """Draws and displays board of current game state using pygame."""

    # draw Connect Four slots
    for col_num in range(constants.COLUMN_COUNT):
        for row_num in range(constants.ROW_COUNT):
            pygame.draw.rect(
                screen,
                constants.COLOR_TO_CODE_DICT["blue"],
                (
                    col_num * constants.SQUARESIZE,
                    (row_num * constants.SQUARESIZE) + constants.SQUARESIZE,
                    constants.SQUARESIZE,
                    constants.SQUARESIZE
                )
            )
            pygame.draw.circle(
                screen,
                constants.COLOR_TO_CODE_DICT["black"],
                int(
                    (col_num * constants.SQUARESIZE)
                    + (constants.SQUARESIZE / 2)
                ),
                int(
                    (row_num * constants.SQUARESIZE)
                    + (1.5 * constants.SQUARESIZE)
                ),
                constants.SLOT_RADIUS
            )

    # draw pieces on the board

    # update display
    pygame.display.update()
