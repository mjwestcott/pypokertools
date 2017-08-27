"""
This module contains simple constants, classes and containers
for working with playing cards in poker analysis.

To create a convenient API for interactive analysis, a subclass of
namedtuple is used to represent cards.
"""

from collections import namedtuple

#------------------------------------------------------------------------------
# Constants


# Note: there is some redundancy in HOLECARDS_NAMES below in that the list
# contains both "Ah 2h" and "2h Ah". This is deliberate. This library was
# designed to be used interactively and as such the convenience of accessing
# holecards by either name is more important than efficiency. For a canonical
# list of names see translation.py

SUITS = "cdhs"
RANKS = "23456789TJQKA"
NUM_CARDS = 52

# A list of 52 strings in the form ["2c", "3c", 4c", ..., "As"]
CARD_NAMES = [
    "{}{}".format(r, s)
    for s in SUITS
    for r in RANKS
]
# A list of 2652 strings in the form ["2c 3c", "2c 4c", ..., "As Ks"]
HOLECARDS_NAMES = [
    "{} {}".format(c1, c2)
    for c1 in CARD_NAMES
    for c2 in CARD_NAMES
    if c1 != c2
]

# Dicts to translate ranks from str to int and vice versa
STR_TO_NUM = dict(zip(RANKS, range(2, 15)))
NUM_TO_STR = dict(zip(range(2, 15), RANKS))


#------------------------------------------------------------------------------
# Classes


class Card(namedtuple("Card", ["name", "rank", "suit", "numerical_rank"])):
    """
    A playing card.

    Should be accessed via the `CARDS` container available in this module,
    which is a dictionary of pre-built Card objects.

    Attributes:
        name (str): e.g. "Kh", "2s", etc. Satisfies the regex [2-9TJQKA][cdhs]
        rank (str): e.g. "K", "2", etc. Equivalent to name[0]
        suit (str): e.g. "c", "d", etc. Equivalent to name[1]
        numerical_rank (int): Values 2-14; a numerical equivalent of its rank

    Examples:
        >>> CARDS["As"]
        <Card: As>
        >>> CARDS["Jh"].numerical_rank
        11
    """
    __slots__ = ()

    # We want the sorting of cards to follow the conventions of poker,
    # according to which cards are compared by their numerical rank. When they
    # have the same rank, the suit can break the tie. Suits have no intrinsic
    # value and so we use an alphabetical comparison.
    def __lt__(self, other):
        if self.numerical_rank == other.numerical_rank:
            return self.suit < other.suit
        return self.numerical_rank < other.numerical_rank

    def __le__(self, other):
        if self.numerical_rank == other.numerical_rank:
            return self.suit <= other.suit
        return self.numerical_rank <= other.numerical_rank

    def __gt__(self, other):
        if self.numerical_rank == other.numerical_rank:
            return self.suit > other.suit
        return self.numerical_rank > other.numerical_rank

    def __ge__(self, other):
        if self.numerical_rank == other.numerical_rank:
            return self.suit >= other.suit
        return self.numerical_rank >= other.numerical_rank

    def __repr__(self):
        return "<Card: {}>".format(self.name)


#------------------------------------------------------------------------------
# Making the Containers


def get_numerical_rank(str_rank):
    return STR_TO_NUM[str_rank]


def get_string_rank(num_rank):
    return NUM_TO_STR[num_rank]


def _make_cards_dict():
    ranks = [n[0] for n in CARD_NAMES]
    suits = [n[1] for n in CARD_NAMES]
    numerical_ranks = [get_numerical_rank(r) for r in ranks]
    return {
        name: Card(name, rank, suit, numerical_rank)
        for name, rank, suit, numerical_rank
        in zip(CARD_NAMES, ranks, suits, numerical_ranks)
    }


# Holecards are simply pairs of cards.
def _make_holecards_dict():
    holecards_list = [
        (CARDS[x], CARDS[y])
        for x in CARD_NAMES
        for y in CARD_NAMES
        if x != y
    ]
    return {
        name: holecards
        for name, holecards
        in zip(HOLECARDS_NAMES, holecards_list)
    }

# Accessible by string name, e.g.
# CARDS["As"], HOLECARDS["Ah Jh"]
CARDS = _make_cards_dict()
HOLECARDS = _make_holecards_dict()


#------------------------------------------------------------------------------
# Utils


def cards_from_str(names):
    """
    Given a string with space-separated card names, return
    a list of Card objects representing a 5-card hand.

    >>> cards_from_str('4h 5h 6h 7h 8h')
    [<Card: 4h>, <Card: 5h>, <Card: 6h>, <Card: 7h>, <Card: 8h>]
    """
    return [CARDS[name] for name in names.split()]
