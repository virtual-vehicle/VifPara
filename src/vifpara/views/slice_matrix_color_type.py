from enum import IntEnum


class SliceMatrixColorType(IntEnum):
    """ A single color bar at the bottom of the matrix."""
    COLOR_CENTERED = 0
    """ A color bar at the bottom of the matrix for each column. """
    COLOR_PER_COLUMN = 1
    """ A color bar for each individual view. Is rendered below the regarding view."""
    COLOR_FOR_EACH = 2
    """ No color bar rendered for the views."""
    COLOR_NONE = 3
