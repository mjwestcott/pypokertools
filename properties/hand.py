from pokertools import (
    sorted_count_of_values,
    sorted_numerical_ranks,
    num_suits,
)


def is_straightflush(hand):
    return is_flush(hand) and is_straight(hand)


def is_fourofakind(hand):
    return sorted_count_of_values(hand) == [4, 1]


def is_fullhouse(hand):
    return sorted_count_of_values(hand) == [3, 2]


def is_flush(hand):
    return num_suits(hand) == 1


def is_straight(hand):
    ranks = sorted_numerical_ranks(hand)

    # Special case for Ace playing low
    if ranks == [2, 3, 4, 5, 14]:
        return True
    return (
        max(ranks) - min(ranks) == 4
        and sorted_count_of_values(hand) == [1, 1, 1, 1, 1]
    )


def is_threeofakind(hand):
    return sorted_count_of_values(hand) == [3, 1, 1]


def is_twopair(hand):
    return sorted_count_of_values(hand) == [2, 2, 1]


def is_onepair(hand):
    return sorted_count_of_values(hand) == [2, 1, 1, 1]


def is_nopair(hand):
    # 'No pair' means 'not(pair-or-better)'
    return (
        sorted_count_of_values(hand) == [1, 1, 1, 1, 1]
        and is_straight(hand) is False
        and is_flush(hand) is False
    )


def is_pair_or_better(hand):
    return not is_nopair(hand)


def is_twopair_or_better(hand):
    return (
        is_twopair(hand)
        or is_threeofakind(hand)
        or is_flush(hand)
        or is_straight(hand)
        or is_fullhouse(hand)
        or is_fourofakind(hand)
    )
