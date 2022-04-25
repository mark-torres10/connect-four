"""Main file, to manage gameplay."""
import math
import sys

import pygame

# TODO(mark): when board is displayed, it needs to be flipped.
# we can represent the coordinates correctly in a matrix, but the
# board will be drawn upside down unless it's flipped.
from components import Board
from constants import (
    COLOR_TO_CODE_DICT,
    COLUMN_COUNT,
    GAME_WIDTH,
    ROW_COUNT,
    SLOT_RADIUS,
    SQUARESIZE,
    VALUE_TO_COLOR_DICT
)
from helper_play_game import (
    draw_board, init_game
)

pygame.init()
pygame.font.init()

GAME_STATUS_FONT = pygame.font.SysFont("monospace", 80)

GAME_OVER_BOOL = False

IS_PLAYER_1_TURN = True

# 20 second wait interval after finishing game.
TIME_TO_WAIT = 20000


def play_game():
    """Main function to play game."""
    screen = init_game()
    board = Board(num_rows=ROW_COUNT, num_columns=COLUMN_COUNT)
    board.init_board()
    global IS_PLAYER_1_TURN
    global GAME_STATUS_FONT
    global GAME_OVER_BOOL
    draw_board(board=board, screen=screen)
    pygame.display.update()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            # render piece while user is hovering on screen.
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(
                    screen,
                    COLOR_TO_CODE_DICT["black"],
                    (0, 0, GAME_WIDTH, SQUARESIZE)
                )
                posx = event.pos[0]
                if IS_PLAYER_1_TURN:
                    pygame.draw.circle(
                        screen,
                        COLOR_TO_CODE_DICT[VALUE_TO_COLOR_DICT[1]],
                        (posx, int(SQUARESIZE / 2)),
                        SLOT_RADIUS
                    )
                else:
                    pygame.draw.circle(
                        screen,
                        COLOR_TO_CODE_DICT[VALUE_TO_COLOR_DICT[2]],
                        (posx, int(SQUARESIZE / 2)),
                        SLOT_RADIUS
                    )

            pygame.display.update()

            # drop piece when mouse is clicked.
            if event.type == pygame.MOUSEBUTTONDOWN:

                # if game is over, don't do anything but draw current state.
                if GAME_OVER_BOOL:
                    draw_board(board=board, screen=screen)

                else:
                    pygame.draw.rect(
                        screen,
                        COLOR_TO_CODE_DICT["black"],
                        (0, 0, GAME_WIDTH, SQUARESIZE)
                    )
                    posx = event.pos[0]
                    col_num = math.floor(posx / SQUARESIZE) - 1
                    print(col_num)

                    if col_num > 0 and col_num < board.num_columns:
                        is_successful_move = False

                        value_of_piece = 1 if IS_PLAYER_1_TURN else 2

                        while not is_successful_move:
                            has_move_succeeded = board.drop_piece(
                                col_num=col_num, value=value_of_piece
                            )
                            is_successful_move = has_move_succeeded

                        draw_board(board=board, screen=screen)
                        IS_PLAYER_1_TURN = not IS_PLAYER_1_TURN

                        is_game_over, winner = board.is_game_over()

                        if is_game_over:
                            if winner:
                                label = pygame.font.Font.render(
                                    GAME_STATUS_FONT,
                                    f"Player {int(winner)} wins!",
                                    COLOR_TO_CODE_DICT[
                                        VALUE_TO_COLOR_DICT[winner]
                                    ],
                                    COLOR_TO_CODE_DICT["white"]
                                )
                                screen.blit(label, (40, 10))
                            else:
                                screen.blit("It's a draw!", (40, 10))

                            draw_board(board=board, screen=screen)
                            pygame.time.wait(3000)

                            GAME_OVER_BOOL = True


if __name__ == '__main__':
    # TODO(mark): need to handle game resets
    play_game()
