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
    - they have three-to-a-flush using both hole cards,
    - they have three-to-a-straight using both hole cards, and
    - they do not have a pair or better.
Expert poker players will recognise these as good candidates to use as bluffs.
"""

from collections import Counter
from functools import wraps
from itertools import chain

import pokertools

#------------------------------------------------------------------------------
# Standard Hand Properties


def sorted_count_of_values(hand):
    """
    Takes a list of five pokertools.Card objects and returns a sorted
    list of counts of the card ranks.

    For example, consider this hand:
        [<Card: 7h>, <Card: Ks>, <Card: 7d>, <Card: 7c>, <Card: Kd>]
    Its corresponding list of numerical ranks is:
        [7, 13, 7, 7, 13].
    Counting each element and sorting returns:
        [3, 2].
    This is a pattern we can use to determine hand properties.
    """
    list_of_ranks = [card.numerical_rank for card in hand]
    return sorted(Counter(list_of_ranks).values(), reverse=True)


# Each function below finds standard poker hands. Each takes a list of five
# pokertools.Card objects and returns a bool. They are doctested at the end of
# the module


def is_straightflush(hand):
    return is_flush(hand) and is_straight(hand)


def is_fourofakind(hand):
    return sorted_count_of_values(hand) == [4, 1]


def is_fullhouse(hand):
    return sorted_count_of_values(hand) == [3, 2]


def is_flush(hand):
    return len(set([card.suit for card in hand])) == 1


def is_straight(hand):
    numerical_ranks = sorted([card.numerical_rank for card in hand])

    # Special case for Ace playing low
    if numerical_ranks == [2, 3, 4, 5, 14]:
        return True
    return (
        max(numerical_ranks) - min(numerical_ranks) == 4
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

#------------------------------------------------------------------------------
# Complex Hand Propeties
#
# In this section it is important to keep track of our holecards. As a
# result, these functions accept two positional arguments:
#     - holecards, a list of two cards
#     - flop, a list of three cards
# We can use this decorator to ensure that these arguments, when flattened
# by itertools.chain, comprise exactly five non-conflicting cards.


def five_cards(f):
    """
    A decorator to check that a function is passed exactly five cards
    in its positional arguments.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        cards = list(chain(*args))
        n = len(cards)
        if n != 5:
            raise ValueError("Exactly five cards must be passed to {}".format(f.__name__))
        if n != len(set(cards)):
            raise ValueError("Conflicting cards passed to {}".format(f.__name__))
        return f(*args, **kwargs)
    return wrapper


@five_cards
def is_3straight(holecards, flop, required_holecards=2):
    """
    Returns a bool indicating whether our holecards have three-to-a-straight
    on this flop. Three-to-a-straight means that there exists a combination of
    three of the five total cards that is consecutive in rank.

    (Specify how many of our holecards must be part of the combination using
    required_holecards.  Default is 2 since this is intended to represent a
    property of those holecards that make it a good candidate for bluffing. A
    value 1 means at least 1.)

    Args:
        holecards (list): two pokertools.Card objects
        flop (list): three pokertools.Card objects

    Kwargs:
        required_holecards (int): from 0-2 specifying how many of our
            holecards are required to satisfy the property.

    Returns:
        True if the hand has the property three-to-a-straight on this flop
            with the required number of holecards;
        False otherwise

    Examples:
        >>> from pokertools import CARDS, HOLECARDS
        >>> my_holecards = HOLECARDS['4d 5c']
        >>> flop = [CARDS['Qd'], CARDS['3h'], CARDS['Kh']]
        >>> is_3straight(my_holecards, flop)
        True

        >>> my_holecards = HOLECARDS['2h 3c']
        >>> flop = [CARDS['8h'], CARDS['7h'], CARDS['6h']]
        >>> is_3straight(my_holecards, flop)
        False
    """
    assert 0 <= required_holecards <= 2

    rank1, rank2 = [card.numerical_rank for card in holecards]
    hand = list(chain(holecards, flop))
    hand_ranks = sorted([card.numerical_rank for card in hand])

    if hand_ranks[4] == 14:
        # If there's an ace in the hand, it can play high and low
        # for the purpose of making a 3straight, so we insert 1
        # at the leftmost position in the list.
        hand_ranks.insert(0, 1)

    # For each three-length subsequence...
    for i in range(len(hand_ranks) - 2):
        subseq = hand_ranks[i:i+3]

        # Check if it's a straight.
        if subseq[0] == subseq[1] - 1 == subseq[2] - 2:
            if required_holecards == 2:
                if (rank1 in subseq and rank2 in subseq):
                    return True
            elif required_holecards == 1:
                if (rank1 in subseq or rank2 in subseq):
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

    (Specify how many of our holecards must be part of the combination using
    required_holecards. Default is 2 since this is intended to represent a
    property of those holecards that make it a good candidate for bluffing. A
    value 1 means at least 1.)

    Args:
        holecards (list): two pokertools.Card objects
        flop (list): three pokertools.Card objects

    Kwargs:
        required_holecards (int): from 0-2 specifying how many of our
            holecards are required to satisfy the property

    Returns:
        True if holecards has the property three-to-a-flush on this flop;
        False otherwise

    Examples:
        >>> from pokertools import CARDS, HOLECARDS
        >>> my_holecards = HOLECARDS['2d 3d']
        >>> flop = [CARDS['7d'], CARDS['Qh'], CARDS['Kh']]
        >>> is_3flush(my_holecards, flop)
        True

        >>> my_holecards = HOLECARDS['2h 3d']
        >>> flop = [CARDS['7h'], CARDS['Ah'], CARDS['Kd']]
        >>> is_3flush(my_holecards, flop)
        False
    """
    assert 0 <= required_holecards <= 2

    suit1, suit2 = [card.suit for card in holecards]
    hand = list(chain(holecards, flop))
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
        - three-to-a-flush using both hole cards       (see is_3flush())
        - three-to-a-straight using both hole cards    (see is_3straight())
        - not(pair-or-better)                          (see is_nopair())

    Args:
        holecards (list): two pokertools.Card objects
        flop (list): three pokertools.Card objects

    Returns:
        True if holecards has the properties listed above on this flop;
        False otherwise

    Example:
        >>> from pokertools import CARDS, HOLECARDS
        >>> my_holecards = HOLECARDS['2d 3d']
        >>> flop = [CARDS['7d'], CARDS['As'], CARDS['Kh']]
        >>> is_bluffcandidate(my_holecards, flop)
        True

        >>> my_holecards = HOLECARDS['2h 3c']
        >>> flop = [CARDS['8h'], CARDS['7h'], CARDS['6h']]
        >>> is_bluffcandidate(my_holecards, flop)
        False
    """
    hand = list(chain(holecards, flop))
    return (
        is_nopair(hand)
        and is_3flush(holecards, flop, required_holecards=2)
        and is_3straight(holecards, flop, required_holecards=2)
    )

#------------------------------------------------------------------------------
# doctests

__doc__ += """
>>> from pokertools import CARDS, HOLECARDS
>>> my_holecards = HOLECARDS['Qs Js']
>>> flop = [CARDS['7s'], CARDS['Td'], CARDS['2d']]
>>> is_bluffcandidate(my_holecards, flop)
True

>>> my_holecards = HOLECARDS['Qs Js']
>>> flop = [CARDS['As'], CARDS['Td'], CARDS['Kd']]
>>> is_bluffcandidate(my_holecards, flop)
False

>>> my_holecards = HOLECARDS['9h 2c']
>>> flop = [CARDS['8h'], CARDS['7h'], CARDS['Kh']]
>>> is_3straight(my_holecards, flop, required_holecards=1)
True

>>> my_holecards = HOLECARDS['2h 3d']
>>> flop = [CARDS['7h'], CARDS['Ah'], CARDS['Kd']]
>>> is_3flush(my_holecards, flop, required_holecards=1)
True

>>> my_holecards = HOLECARDS['7s 6s']
>>> flop = [CARDS['Ts'], CARDS['9s'], CARDS['8s']]
>>> hand = list(chain(my_holecards, flop))
>>> is_straightflush(hand)
True

>>> hand = [CARDS['3s'], CARDS['Js'], CARDS['Jc'], CARDS['Jd'], CARDS['Jh']]
>>> is_fourofakind(hand)
True

>>> hand = [CARDS['3s'], CARDS['Js'], CARDS['Jc'], CARDS['Jd'], CARDS['2d']]
>>> is_threeofakind(hand)
True

>>> hand = [CARDS['6s'], CARDS['7s'], CARDS['6c'], CARDS['2d'], CARDS['7d']]
>>> is_twopair(hand)
True

>>> hand = [CARDS['2s'], CARDS['2h'], CARDS['Ac'], CARDS['Ks'], CARDS['Qh']]
>>> is_onepair(hand)
True

>>> my_holecards = HOLECARDS['As 7s']
>>> flop = [CARDS['6c'], CARDS['2d'], CARDS['Qd']]
>>> hand = list(chain(my_holecards, flop))
>>> is_nopair(hand)
True

>>> my_holecards = HOLECARDS['Qs Js']
>>> flop = [CARDS['Qs'], CARDS['2d'], CARDS['2d']]
>>> is_bluffcandidate(my_holecards, flop)
Traceback (most recent call last):
    ...
ValueError: Conflicting cards passed to is_bluffcandidate

>>> my_holecards = HOLECARDS['As Ad']
>>> flop = [CARDS['7s'], CARDS['Td'], CARDS['2d'], CARDS['Ah']]
>>> is_bluffcandidate(my_holecards, flop)
Traceback (most recent call last):
    ...
ValueError: Exactly five cards must be passed to is_bluffcandidate
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()
