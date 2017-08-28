"""
What properties does my hand have on the flop?

Poker analysis libraries commonly classify five-card poker hands according to a
scheme which allows two hands to be compared at showdown; they can find whether
my hand is a pair, straight, or flush etc., and rank them accordingly. This is
useful on the river when hand strengths are final.

However, on the flop things are different. First, there are many more
properties that may be of interest: whether we have a draw (and whether it's a
draw to the nuts), whether we have two overcards, etc. Second, some properties,
such as having 'three-to-a-straight' dont require all five cards, in which case
we want to know whether the property is the result of using _both_ our
holecards.

In this module you will find functions to find hands which satisfy these three
properties:
    - they do not have a pair or better (unless it's only on the board).
    - they have three-to-a-flush using both hole cards,
    - they have three-to-a-straight using both hole cards, and
Expert poker players will recognise these as good candidates to use as bluffs.
"""
from collections import Counter
from functools import wraps
from itertools import chain

from pokertools import (
    CANONICAL_HOLECARDS,
    sorted_numerical_ranks,
)
from properties.hand import is_onepair as hand_is_onepair
from properties.hand import is_twopair_or_better as hand_is_twopair_or_better
from properties.holecards import is_pair as is_pocket_pair


#------------------------------------------------------------------------------
# Complex Hand Propeties
#
# In this section it is important to keep track of our holecards. As a
# result, these functions accept two positional arguments:
#     - holecards, a tuple of two cards
#     - flop, a tuple of three cards
# We can use this decorator to ensure that these arguments, when flattened
# by itertools.chain, comprise exactly five non-conflicting cards.


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


@five_cards
def is_onepair(holecards, flop, required_holecards=1):
    """
    Returns a bool indicating whether our holecards have made one pair
    on this flop.
    """
    assert 0 <= required_holecards <= 2
    hand = tuple(chain(holecards, flop))

    if required_holecards == 2:
        return is_pocket_pair(holecards)
    elif required_holecards == 1:
        rank1, rank2 = sorted_numerical_ranks(holecards)
        rank_counts = Counter([card.numerical_rank for card in hand])
        return (
            rank_counts[rank1] == 2 or rank_counts[rank2] == 2
            and hand_is_onepair(hand)
        )
    elif required_holecards == 0:
        return hand_is_onepair(hand)


@five_cards
def is_3straight(holecards, flop, required_holecards=2):
    """
    Returns a bool indicating whether our holecards have three-to-a-straight
    on this flop. Three-to-a-straight means that there exists a combination of
    three of the five total cards that is consecutive in rank.
    """
    assert 0 <= required_holecards <= 2

    rank1, rank2 = sorted_numerical_ranks(holecards)
    hand = tuple(chain(holecards, flop))
    ranks = sorted_numerical_ranks(hand)

    def subseqs():
        for i in range(len(ranks) - 2):
            yield ranks[i:i + 3]
        a, b, _, _, c = ranks  # Special case for Ace playing low
        if [a, b, c] == [2, 3, 14]:
            yield [a, b, c]

    for subseq in subseqs():
        x, y, z = subseq
        if x == y-1 == z-2 or [x, y, z] == [2, 3, 14]:
            if required_holecards == 2:
                if rank1 in subseq and rank2 in subseq:
                    return True
            elif required_holecards == 1:
                if rank1 in subseq or rank2 in subseq:
                    return True
            elif required_holecards == 0:
                return True
    return False


@five_cards
def is_3flush(holecards, flop, required_holecards=2):
    """
    Returns a bool indicating whether our holecards have three-to-a-flush
    on this flop. Three-to-a-flush means that there exists a combination of
    three of the five total cards which have the same suit.
    """
    assert 0 <= required_holecards <= 2

    suit1, suit2 = [card.suit for card in holecards]
    hand = tuple(chain(holecards, flop))
    suit_counts = Counter([card.suit for card in hand])

    for suit in suit_counts:
        if suit_counts[suit] == 3:
            if required_holecards == 2 and (suit1 == suit2 == suit):
                return True
            elif required_holecards == 1:
                if (suit1 == suit or suit2 == suit):
                    return True
            elif required_holecards == 0:
                return True
    return False

#------------------------------------------------------------------------------
# Bluff Candidates


@five_cards
def is_bluffcandidate(holecards, flop):
    """
    Returns a bool indicating whether our holecards are a good
    candidate for bluffing.

    Checks whether our hand has three properties:
        - not(pair-or-better) using at least one holecard
        - three-to-a-flush using both hole cards
        - three-to-a-straight using both hole cards

    Example:
        >>> from pokertools import cards_from_str
        >>> holecards = flop = cards_from_str
        >>> assert holecards('Qd Jd') in set(get_bluffcandidates(flop('Kc 2d 2h')))
        >>> assert holecards('8s 7s') in set(get_bluffcandidates(flop('9c 4s 3d')))
        >>> assert holecards('Kc Jc') in set(get_bluffcandidates(flop('Qc 8d 3h')))
    """
    hand = tuple(chain(holecards, flop))
    return (
        not is_onepair(holecards, flop, required_holecards=1)
        and not hand_is_twopair_or_better(hand)
        and is_3flush(holecards, flop, required_holecards=2)
        and is_3straight(holecards, flop, required_holecards=2)
    )


def get_bluffcandidates(flop):
    for holecards in CANONICAL_HOLECARDS.values():
        try:
            if is_bluffcandidate(holecards, flop):
                yield holecards
        except ConflictingCards:
            pass
