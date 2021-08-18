"""
This module contains simple constants, classes and containers
for working with playing cards in poker analysis.

To create a convenient API for interactive analysis, a subclass of
namedtuple is used to represent cards.
"""
import random
from collections import Counter, namedtuple
from functools import lru_cache, wraps
from itertools import chain, combinations, permutations

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
# We prefer the former: its first card has the higher rank.
CANONICAL_HOLECARDS_NAMES = {
    "{} {}".format(CARD_NAMES[i], CARD_NAMES[j])
    for i in range(NUM_CARDS)
    for j in range(i+1, NUM_CARDS)
}

RANK_STR_TO_NUM = dict(zip(RANKS, NUMERICAL_RANKS))
RANK_NUM_TO_STR = dict(zip(NUMERICAL_RANKS, RANKS))

SUIT_PERMUTATIONS = list(permutations(SUITS, r=2))
SUIT_COMBINATIONS = list(combinations(SUITS, r=2))

FLOP_NAMES = ["{} {} {}".format(*x) for x in combinations(CARD_NAMES, r=3)]


class Card(namedtuple("Card", ["name", "numerical_rank"])):
    """
    A playing card.

    Attributes:
        Card.name (str): eg. "Kh", "2s", etc. Satisfies the regex [2-9TJQKA][cdhs]
        Card.rank (str): eg. "K", "2", etc. Equivalent to name[0]
        Card.suit (str): eg. "c", "d", etc. Equivalent to name[1]
        Card.numerical_rank (int): Values 2-14; a numerical equivalent of its rank

    Examples:
        >>> CARDS["As"]
        <Card: As>
        >>> CARDS["Jh"].numerical_rank
        11
    """
    __slots__ = ()

    @property
    def rank(self):
        return self.name[0]

    @property
    def suit(self):
        return self.name[1]

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

    def pretty_print(self):
        if self.suit == 'c':
            unicode_suit = '\u2663'
        elif self.suit == 'd':
            unicode_suit = '\u2666'
        elif self.suit == 'h':
            unicode_suit = '\u2665'
        else:
            unicode_suit = '\u2660'

        return f"{self.rank}{unicode_suit}"

    def color_pretty_print(self):
        if self.suit == 'c':
            unicode_suit = '\u2663'
            color = 'green'
        elif self.suit == 'd':
            unicode_suit = '\u2666'
            color = 'blue'
        elif self.suit == 'h':
            unicode_suit = '\u2665'
            color = 'red'
        else:
            unicode_suit = '\u2660'
            color = 'black'

        return f"<font color=\"{color}\">{self.rank}{unicode_suit}</font>"


# ------------------------------------------------------------------------------
# Making the Containers


get_string_rank = RANK_NUM_TO_STR.__getitem__
get_numerical_rank = RANK_STR_TO_NUM.__getitem__


def _make_cards_dict():
    numerical_ranks = [get_numerical_rank(name[0]) for name in CARD_NAMES]
    return {
        name: Card(name, numerical_rank)
        for name, numerical_rank
        in zip(CARD_NAMES, numerical_ranks)
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
        name: holecards_
        for name, holecards_
        in zip(HOLECARDS_NAMES, holecards_list)
    }


# Accessible by string name, e.g. CARDS["As"], HOLECARDS["Ah Jh"]
CARDS = _make_cards_dict()
HOLECARDS = _make_holecards_dict()
CANONICAL_HOLECARDS = {k: HOLECARDS[k] for k in CANONICAL_HOLECARDS_NAMES}

# 1326 canonical holecards ordered in a PioSolver manner,
# eg. obtained by show_hand_order command sent to PioSolver
PIO_HOLECARDS_ORDER = sorted([tuple(sorted(holecard, reverse=True))
                              for holecard in CANONICAL_HOLECARDS.values()
                              ])

PIO_HOLECARDS_INDICES = {holecard: i for i, holecard in enumerate(PIO_HOLECARDS_ORDER)}


def cards_from_str(names):
    """
    Given a string with space-separated card names, return
    a tuple of Card objects.

    >>> cards_from_str('4h 5h 6h 7h 8h')
    (<Card: 4h>, <Card: 5h>, <Card: 6h>, <Card: 7h>, <Card: 8h>)
    """
    return tuple(CARDS[name] for name in names.split())


# These aliases allow us to create tuples of cards easily, while also describing
# the intended use. They constitute the main interface provided by this module.
holecards = flop = hand = cards_from_str


# ------------------------------------------------------------------------------
# Utils


class ConflictingCards(Exception):
    pass


def five_cards(f):
    """
    A decorator to check that a function is passed exactly five cards
    in its positional arguments.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        cards = tuple(chain(*args))
        n = len(cards)
        if n != 5:
            raise ValueError("Exactly five cards must be passed to {}".format(f.__name__))
        if n != len(set(cards)):
            raise ConflictingCards("Conflicting cards passed to {}: {}".format(f.__name__, cards))
        return f(*args, **kwargs)
    return wrapper


def remove_conflicts(iterable):
    """
    Given an iterable of (holecards, flop), filter out hands with conflicts.
    """
    for holecards_, flop_ in iterable:
        if len(set(chain(holecards_, flop_))) == 5:
            yield holecards_, flop_


def no_conflicts(holecards_, flop_):
    """
    Checks if there are no conflicting cards among given iterables.
    :param holecards_: iterable of holecards Card items
    :param flop_: iterable of flop or generally board Card items
    :return: Returns true if there are no conflicting cards.
    """
    return len(set(chain(holecards_, flop_))) == len(list(chain(holecards_, flop_)))


def make_deck():
    cards = list(CARDS.values())
    random.shuffle(cards)
    return cards


def deal(deck, n=1):
    if n == 1:
        return deck.pop()
    return tuple(deck.pop() for _ in range(n))


memoize = lru_cache(maxsize=None)


@memoize
def sorted_count_of_values(cards):
    """
    Takes a tuple of pokertools.Card objects and returns a sorted
    list of counts of the card ranks.

    For example, consider this hand:
        hand('7h Ks 7d 7c Kd')
    Its corresponding list of numerical ranks is:
        [7, 13, 7, 7, 13].
    Counting each element and sorting returns:
        [3, 2].
    This is a pattern we can use to determine hand properties.
    """
    list_of_ranks = [card.numerical_rank for card in cards]
    return sorted(Counter(list_of_ranks).values(), reverse=True)


@memoize
def sorted_numerical_ranks(cards):
    return sorted([card.numerical_rank for card in cards])


@memoize
def num_suits(cards):
    return len(set(card.suit for card in cards))


@memoize
def rank_subsequences(hand_):
    """
    Given a five-card hand, generate all three-length subsequences of the ranks
    accounting for the fact that an Ace can play low (as rank 1 as well as 14).
    """
    ranks = sorted_numerical_ranks(hand_)
    for i in range(3):
        yield ranks[i:i + 3]

    # Special case for Ace playing low
    a, b, c, d, e = ranks
    if e == 14:
        ranks = [1, a, b, c, d]
        for i in range(3):
            yield ranks[i:i + 3]
