from pypokertools.pokertools import (
    num_suits,
    sorted_count_of_values,
    sorted_numerical_ranks,
)

#------------------------------------------------------------------------------
# Properties of flops


def is_rainbow(flop):
    return num_suits(flop) == 3


def is_monotone(flop):
    return num_suits(flop) == 1


def has_2flush(flop):
    return num_suits(flop) == 2


def has_pair(flop):
    return sorted_count_of_values(flop) == [2, 1]


def has_threeofakind(flop):
    return sorted_count_of_values(flop) == [3]


def has_3straight(flop):
    ranks = sorted_numerical_ranks(flop)

    # Special case for Ace playing low
    if ranks == [2, 3, 14]:
        return True
    return (
        max(ranks) - min(ranks) == 2
        and sorted_count_of_values(flop) == [1, 1, 1]
    )


def has_gutshot(flop):
    ranks = sorted_numerical_ranks(flop)

    # Special case for Ace playing low
    if ranks == [2, 4, 14] or ranks == [3, 4, 14]:
        return True
    return (
        max(ranks) - min(ranks) == 3
        and sorted_count_of_values(flop) == [1, 1, 1]
    )
