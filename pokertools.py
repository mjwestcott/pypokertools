"""
This module contains simple constants, classes and containers
for working with playing cards in poker analysis.

To create a convenient API for interactive analysis, a subclass of
namedtuple is used to represent cards.
"""
import random
from collections import namedtuple, Counter
from itertools import combinations, permutations

#------------------------------------------------------------------------------
# Constants


SUITS = "cdhs"
RANKS = "23456789TJQKA"
NUMERICAL_RANKS = range(2, 15)
NUM_CARDS = 52

# A list of 52 strings in the form ["Ac", "Ad", Ah", ..., "2s"]
# ordered by highest rank.
CARD_NAMES = [
    "{}{}".format(r, s)
    for r in reversed(RANKS)
    for s in SUITS
]
# A list of 2652 strings in the form ["Ac Kc", "Ac Qc", ..., "3s 2s"]
HOLECARDS_NAMES = [
    "{} {}".format(c1, c2)
    for c1 in CARD_NAMES
    for c2 in CARD_NAMES
    if c1 != c2
]
# Sometimes -- e.g. for the purpose of storing a range of holecards --
# position-isomorphs are irrelevant; "Ah Kc" is the same as "Kc Ah".
# We prefer to former: it's first card has the higher rank.
CANONICAL_HOLECARDS_NAMES = {
    "{} {}".format(CARD_NAMES[i], CARD_NAMES[j])
    for i in range(NUM_CARDS)
    for j in range(i+1, NUM_CARDS)
}

RANK_STR_TO_NUM = dict(zip(RANKS, NUMERICAL_RANKS))
RANK_NUM_TO_STR = dict(zip(NUMERICAL_RANKS, RANKS))

SUIT_PERMUATIONS = list(permutations(SUITS, r=2))
SUIT_COMBINATIONS = list(combinations(SUITS, r=2))


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


get_string_rank = RANK_NUM_TO_STR.__getitem__
get_numerical_rank = RANK_STR_TO_NUM.__getitem__


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

# Accessible by string name, e.g. CARDS["As"], HOLECARDS["Ah Jh"]
CARDS = _make_cards_dict()
HOLECARDS = _make_holecards_dict()
CANONICAL_HOLECARDS = {k: HOLECARDS[k] for k in CANONICAL_HOLECARDS_NAMES}


#------------------------------------------------------------------------------
# Utils


def make_deck():
    cards = list(CARDS.values())
    random.shuffle(cards)
    return cards


def deal(deck, n=1):
    if n == 1:
        return deck.pop()
    return tuple(deck.pop() for _ in range(n))


def cards_from_str(names):
    """
    Given a string with space-separated card names, return
    a list of Card objects representing a 5-card hand.

    >>> cards_from_str('4h 5h 6h 7h 8h')
    [<Card: 4h>, <Card: 5h>, <Card: 6h>, <Card: 7h>, <Card: 8h>]
    """
    return [CARDS[name] for name in names.split()]


def sorted_count_of_values(cards):
    """
    Takes a list of pokertools.Card objects and returns a sorted
    list of counts of the card ranks.

    For example, consider this hand:
        [<Card: 7h>, <Card: Ks>, <Card: 7d>, <Card: 7c>, <Card: Kd>]
    Its corresponding list of numerical ranks is:
        [7, 13, 7, 7, 13].
    Counting each element and sorting returns:
        [3, 2].
    This is a pattern we can use to determine hand properties.
    """
    list_of_ranks = [card.numerical_rank for card in cards]
    return sorted(Counter(list_of_ranks).values(), reverse=True)


def sorted_numerical_ranks(cards):
    return sorted([card.numerical_rank for card in cards])


def num_suits(cards):
    return len(set(card.suit for card in cards))
