"""Main file, to manage gameplay."""
import sys

import pygame

# TODO(mark): when board is displayed, it needs to be flipped.
# we can represent the coordinates correctly in a matrix, but the
# board will be drawn upside down unless it's flipped.
from scripts.components import Board
from scripts.helper_play_game import (
    draw_board, init_game
)

GAME_OVER_BOOL = False


def play_game():
    """Main function to play game."""
    screen = init_game()
    board = Board

    draw_board(board=board, screen=screen)
    pygame.display.update()

    while not GAME_OVER_BOOL:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == '__main__':
    play_game()
