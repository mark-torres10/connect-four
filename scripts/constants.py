"""Constants needed for game."""

# NOTE(mark): I might have flipped the row and column counts. Oops.
# should just have to flip these, though I know that I hardcoded certain
# amounts elsewhere and that this will likely have to be addressed.

# NOTE(mark): alternatively, could just flip the board 90 degrees when
# displaying it. This is a jank solution, but probably the easiest to
# implement. I already have to flip it anyways, might as well turn it instead.
# implementation would be:
# (a) do calculations on real table
# (b) create a table that is actually shown to the user, and just have that
# table be a rotated version of the real table.
# (c) update shown table whenever the real table is updated.
ROW_COUNT = 7
COLUMN_COUNT = 6
NUM_IN_A_ROW_TO_WIN = 4

SQUARESIZE = 100
GAME_WIDTH = (COLUMN_COUNT + 3) * SQUARESIZE
GAME_HEIGHT = (ROW_COUNT + 3) * SQUARESIZE

GAME_SIZE = (GAME_WIDTH, GAME_HEIGHT)

SLOT_RADIUS = int(SQUARESIZE / 2 - 8)

COLOR_TO_CODE_DICT = {
    "blue": (0, 0, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "yellow": (255, 255, 0)
}

VALUE_TO_COLOR_DICT = {
    1: "red",
    2: "yellow"
}
