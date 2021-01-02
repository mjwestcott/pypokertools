"""
Finding isomorphic/canonical representations of the flop.

In Texas Holdem suits have no intrinsic value. Thus, if the flop is "2d 3d 4d",
the possible holecards "5c 6c", "5h 6h", and "5s 6s" are equivalent -- they are
each a straight and the suits are irrelevant. Similarly, the flop "4d 3d 2d" is
equivalent to the flop above -- the order of cards is irrelevant. This fact may
be used to dramatically reduce the number of lookup tables required to store
flop equity data; there are 22,100 possible flops, but only 1,755 canonical
versions.

In this module we develop an algorithm for making a list of canonical flops and
also a way to find, for any given randomly generated flop, what its canonical
form is.

For completeness I also include what is, loosely speaking, the opposite
function: a way to produce all suit-isomorphs of a given flop.

Finally, you will find a way to map the suits on the current flop to the suits
on its canonical version. This will allow us to translate the rest of the
current scenario, including our holecards.
"""
from itertools import combinations

from pypokertools.pokertools import CARDS, SUITS

#------------------------------------------------------------------------------
# Finding the Canonical Version
#
# The position-isomorphic aspect of this problem is easy to solve: we can
# simply specify that canonical flops must be sorted. The suit-isomorphic
# aspect is a little more difficult. Suits may appear on the flop in five
# patterns: 'AAA', 'AAB', 'ABA', 'ABB', 'ABC', where the capital letters
# represent arbirary suits. One way to approach this is to specify a canonical
# ordering of suits: that the left-most suit 'A' must be a club, 'B' must be a
# diamond, and 'C' must be a heart. This _almost_ solves the problem elegantly;
# two remaining edge cases are dealt with below.


def get_canonical(flop):
    """
    Returns the canonical version of the given flop.

    Canonical flops are sorted. The first suit is 'c' and, if applicable,
    the second is 'd' and the third is 'h'.

    Args:
        flop (tuple): three pokertools.Card objects

    Returns
        A tuple of three pokertools.Card objects which represent
        the canonical version of the given flop.

    >>> flop = (CARDS['Ks'], CARDS['2c'], CARDS['3s'])
    >>> get_canonical(flop)
    (<Card: 2c>, <Card: 3d>, <Card: Kd>)
    """
    card1, card2, card3 = sorted(flop)
    A, B, C = "cdh"

    if card1.suit == card2.suit == card3.suit:
        return (
            CARDS[card1.rank + A],
            CARDS[card2.rank + A],
            CARDS[card3.rank + A],
        )

    elif card1.suit == card2.suit != card3.suit:
        return (
            CARDS[card1.rank + A],
            CARDS[card2.rank + A],
            CARDS[card3.rank + B],
        )

    elif card1.suit == card3.suit != card2.suit:
        # Special case: if the 2nd and 3rd cards are a pair e.g. the flop is
        # [Jc, Qd, Qc], then our suit changes have resulted in an
        # unsorted flop! The correct canonical form is [Jc, Qc, Qd].
        return tuple(sorted([
            CARDS[card1.rank + A],
            CARDS[card2.rank + B],
            CARDS[card3.rank + A],
        ]))

    elif card1.suit != card2.suit == card3.suit:
        # Special case: if the 1st and 2nd cards are a pair e.g. flop is
        # [2c, 2d, 8d], that is isomorphic with those cards being switched
        # e.g. [2d, 2c, 8d] -- which forms the suit pattern already
        # covered above: 'ABA'. Thus, it can be transformed to [2c, 2d, 8c].
        # This version has higher priority lexicographically -- it has more
        # clubs! To make this change we can simply change the suit of the
        # third card to 'c'.
        if card1.rank == card2.rank:
            return (
                CARDS[card1.rank + A],
                CARDS[card2.rank + B],
                CARDS[card3.rank + A],
            )
        return (
            CARDS[card1.rank + A],
            CARDS[card2.rank + B],
            CARDS[card3.rank + B],
        )

    elif card1.suit != card2.suit != card3.suit:
        return (
            CARDS[card1.rank + A],
            CARDS[card2.rank + B],
            CARDS[card3.rank + C],
        )


def get_all_canonicals():
    """
    Returns the set of all canonical flops. Each flop is a tuple of three
    pokertools.Card objects.
    """
    all_possible_flops = combinations(CARDS.values(), r=3)
    return set(tuple(get_canonical(flop)) for flop in all_possible_flops)


#------------------------------------------------------------------------------
# Suit-Isomorphs


def get_suit_isomorphs(flop):
    """
    Returns a list of all suit-isomorphic combinations of the flop. Each
    flop is a tuple of three pokertools.Card objects.

    >>> flop = (CARDS['As'], CARDS['4s'], CARDS['Ts'])
    >>> for iso in get_suit_isomorphs(flop):
    ...     print(iso)
    (<Card: Ac>, <Card: 4c>, <Card: Tc>)
    (<Card: Ad>, <Card: 4d>, <Card: Td>)
    (<Card: Ah>, <Card: 4h>, <Card: Th>)
    (<Card: As>, <Card: 4s>, <Card: Ts>)

    >>> flop = (CARDS['Kd'], CARDS['Qh'], CARDS['8c'])
    >>> len(get_suit_isomorphs(flop))
    24
    """
    card1, card2, card3 = flop

    if card1.suit == card2.suit == card3.suit:
        # For each suit, produce the suit pattern 'AAA'
        return [
            (
                CARDS[card1.rank + A],
                CARDS[card2.rank + A],
                CARDS[card3.rank + A],
            )
            for A in SUITS
        ]

    elif card1.suit == card2.suit != card3.suit:
        # For each combination of two non-identical
        # suits, produce the suit pattern 'AAB'
        return [
            (
                CARDS[card1.rank + A],
                CARDS[card2.rank + A],
                CARDS[card3.rank + B],
            )
            for A in SUITS for B in SUITS if A != B
        ]

    elif card1.suit != card2.suit == card3.suit:
        # For each combination of two non-identical
        # suits, produce the suit pattern 'ABB'
        return [
            (
                CARDS[card1.rank + A],
                CARDS[card2.rank + B],
                CARDS[card3.rank + B],
            )
            for A in SUITS for B in SUITS if A != B
        ]

    elif card1.suit == card3.suit != card2.suit:
        # For each combination of two non-identical
        # suits, produce the suit pattern 'ABA'
        return [
            (
                CARDS[card1.rank + A],
                CARDS[card2.rank + B],
                CARDS[card3.rank + A],
            )
            for A in SUITS for B in SUITS if A != B
        ]

    elif card1.suit != card2.suit != card3.suit:
        # For each combination of three non-identical
        # suits, produce the suit pattern 'ABC'
        return [
            (
                CARDS[card1.rank + A],
                CARDS[card2.rank + B],
                CARDS[card3.rank + C],
            )
            for A in SUITS for B in SUITS for C in SUITS
            if (A != B and B != C and A != C)
        ]


#------------------------------------------------------------------------------
# Translation Dict


def get_translation_dict(flop):
    """
    Returns a dict which maps suits to other suits. The keys represent the
    suits on the given flop. The values represent the suits on the canonical
    version. This tell us what the 'translation' is between them, allowing us
    to translate the suits of our holecards.

    >>> flop = (CARDS['6h'], CARDS['2d'], CARDS['Qd'])
    >>> get_canonical(flop)
    (<Card: 2c>, <Card: 6d>, <Card: Qc>)
    >>> get_translation_dict(flop) == {'c': 'h', 'd': 'c', 'h': 'd', 's': 's'}
    True
    """
    flop = sorted(flop)
    suit1, suit2, suit3 = [card.suit for card in flop]

    canonical_flop = get_canonical(flop)
    canon1, canon2, canon3 = [card.suit for card in canonical_flop]

    # if the flop matches the canonical version, no translation necessary
    if (suit1, suit2, suit3) == (canon1, canon2, canon3):
        return {"c": "c", "d": "d", "h": "h", "s": "s"}

    unused = {"h", "d", "c", "s"} - {suit1, suit2, suit3}
    canonical_unused = {"h", "d", "c", "s"} - {canon1, canon2, canon3}
    both_unused = unused & canonical_unused

    # listed for indexing the elements, sorted for deterministic output
    unused = sorted(list(unused))
    canonical_unused = sorted(list(canonical_unused))
    both_unused = sorted(list(both_unused))

    if suit1 == suit2 == suit3:
        # suit pattern is 'AAA'
        return {
            suit1: canon1,                   # The first flop suit and the
            canon1: suit1,                   # first canon suit must switch.
            both_unused[0]: both_unused[0],  # The remaining two suits
            both_unused[1]: both_unused[1],  # don't matter
        }

    elif suit1 == suit2 != suit3:
        # suit pattern is 'AAB'
        return {
            suit1: canon1,                   # suit of 1st card = 1st canon
            suit3: canon3,                   # suit of 3rd card = 3rd canon
            unused[0]: canonical_unused[0],  # Must be the remaining two
            unused[1]: canonical_unused[1],  # suits of each set
        }

    elif suit1 != suit2 == suit3:
        # suit pattern is 'ABB'
        return {
            suit1: canon1,                   # suit of 1st card = 1st canon
            suit2: canon2,                   # suit of 2nd card = 2nd canon
            unused[0]: canonical_unused[0],  # Must be the remaining two
            unused[1]: canonical_unused[1],  # suits of each set
        }

    # Note the order of cards
    elif suit1 == suit3 != suit2:
        # suit pattern is 'ABA'
        return {
            suit1: canon1,                   # suit of 1st card = 1st canon
            suit2: canon2,                   # suit of 2nd card = 2nd canon
            unused[0]: canonical_unused[0],  # Must be the remaining two
            unused[1]: canonical_unused[1],  # suits of each set
        }

    elif suit1 != suit2 != suit3:
        # suit pattern is 'ABC'
        return {
            suit1: canon1,                   # suit of 1st card = 1st canon
            suit2: canon2,                   # suit of 2nd card = 2nd canon
            suit3: canon3,                   # suit of 3rd card = 3rd canon
            unused[0]: canonical_unused[0],  # The remaining suits.
        }
