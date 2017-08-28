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
"""
from collections import Counter
from itertools import chain

from pokertools import five_cards, sorted_numerical_ranks, rank_subsequences
from properties.hand import is_onepair as hand_is_onepair
from properties.hand import is_twopair_or_better as hand_is_twopair_or_better
from properties.holecards import is_pair as is_pocket_pair


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
            hand_is_onepair(hand)
            and rank_counts[rank1] == 2 or rank_counts[rank2] == 2
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

    for subseq in rank_subsequences(hand):
        x, y, z = subseq
        if x == y-1 == z-2:
            if x == 1:
                # Special case for Ace playing low, to allow
                # for the `rank in subseq` check to work
                subseq.append(14)
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


@five_cards
def has_two_overcards(holecards, flop):
    """
    Returns a bool indicating whether our holecards have two overcards on this
    flop. Two overcards means both ranks are higher than the highest rank on the
    flop and that our hand is not 'pair-or-better' (unless it's only on the board).
    """
    hand = tuple(chain(holecards, flop))
    flop_ranks = sorted_numerical_ranks(flop)

    return all(
        all(card.numerical_rank > r for r in flop_ranks)
        for card in holecards
    ) and (
        not is_onepair(holecards, flop, required_holecards=1)
        and not hand_is_twopair_or_better(hand)
    )
