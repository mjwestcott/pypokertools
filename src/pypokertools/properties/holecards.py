from pypokertools.pokertools import (
    num_suits,
    sorted_count_of_values,
    sorted_numerical_ranks,
)

#------------------------------------------------------------------------------
# Properties of holecards


def is_pair(holecards):
    return sorted_count_of_values(holecards) == [2]


def is_suited(holecards):
    return num_suits(holecards) == 1


def is_connected(holecards):
    return _gap_size(holecards) == 1


def has_one_gap(holecards):
    return _gap_size(holecards) == 2


def has_two_gap(holecards):
    return _gap_size(holecards) == 3


def _gap_size(holecards):
    a, b = sorted_numerical_ranks(holecards)

    # Special case for Ace playing high or low
    if b == 14:
        high = b - a
        low = a - 1
        return min(high, low)

    return b - a
