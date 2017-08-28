"""
In this module you will find functions to find hands which satisfy these three
properties:
    - they do not have a pair or better (unless it's only on the board).
    - they have three-to-a-flush using both hole cards,
    - they have three-to-a-straight using both hole cards, and
Expert poker players will recognise these as good candidates to use as bluffs.
"""
from itertools import chain

from pokertools import ConflictingCards, CANONICAL_HOLECARDS, five_cards
from properties.hand import is_twopair_or_better as hand_is_twopair_or_better
from properties.complex import is_onepair, is_3flush, is_3straight


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
        >>> from pokertools import holecards, flop
        >>> assert holecards('Qd Jd') in get_bluffcandidates(flop('Kc 2d 2h'))
        >>> assert holecards('8s 7s') in get_bluffcandidates(flop('9c 4s 3d'))
        >>> assert holecards('Kc Jc') in get_bluffcandidates(flop('Qc 8d 3h'))
    """
    hand = tuple(chain(holecards, flop))
    return (
        not is_onepair(holecards, flop, include_board=False)
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
