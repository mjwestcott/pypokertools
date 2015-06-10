"""Finding isomorphic/canonical representations of the flop.

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

# TODO: Think about the best way to scale to turn/river

from pokertools import CARDS, SUITS
from itertools import combinations

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
    """Returns the canonical version of the given flop.

    Canonical flops are sorted. The first suit is 'c' and, if applicable,
    the second is 'd' and the third is 'h'.

    Args:
        flop (list): three pokertools.Card objects

    Returns
        A list of three pokertools.Card objects which represent
        the canonical version of the given flop.

    >>> flop = [CARDS['Ks'], CARDS['2c'], CARDS['3s']]
    >>> get_canonical(flop)
    [<Card: 2c>, <Card: 3d>, <Card: Kd>]
    """

    flop = sorted(flop)
    card1, card2, card3 = flop[0], flop[1], flop[2]

    if card1.suit == card2.suit == card3.suit:    # suit pattern
        return [CARDS[card1.rank + 'c'],          # <-- A
                CARDS[card2.rank + 'c'],          # <-- A
                CARDS[card3.rank + 'c']]          # <-- A

    elif card1.suit == card2.suit != card3.suit:  # suit pattern
        return [CARDS[card1.rank + 'c'],          # <-- A
                CARDS[card2.rank + 'c'],          # <-- A
                CARDS[card3.rank + 'd']]          # <-- B

    elif card1.suit == card3.suit != card2.suit:  # suit pattern
        canonical = [CARDS[card1.rank + 'c'],     # <-- A
                     CARDS[card2.rank + 'd'],     # <-- B
                     CARDS[card3.rank + 'c']]     # <-- A

        # Special case: if the 2nd and 3rd cards are a pair e.g. the flop is
        # [Jc, Qd, Qc], then our suit changes have resulted in an
        # unsorted flop! The correct canonical form is [Jc, Qc, Qd].
        return sorted(canonical)

    elif card1.suit != card2.suit == card3.suit:  # suit pattern
        canonical = [CARDS[card1.rank + 'c'],     # <-- A
                     CARDS[card2.rank + 'd'],     # <-- B
                     CARDS[card3.rank + 'd']]     # <-- B

        # Special case: if the 1st and 2nd cards are a pair e.g. flop is
        # [2c, 2d, 8d], that is isomorphic with those cards being switched
        # e.g. [2d, 2c, 8d] -- which forms the suit pattern already
        # covered above: 'ABA'. Thus, it can be transformed to [2c, 2d, 8c].
        # This version has higher priority lexicographically -- it has more
        # clubs! To make this change we can simply change the suit of the
        # third card to 'c'.
        if canonical[0].rank == canonical[1].rank:
            canonical[2] = CARDS[card3.rank + 'c']
        return canonical

    elif card1.suit != card2.suit != card3.suit:  # suit pattern
        return [CARDS[card1.rank + 'c'],          # <-- A
                CARDS[card2.rank + 'd'],          # <-- B
                CARDS[card3.rank + 'h']]          # <-- C


def get_all_canonicals():
    """Returns the set of all canonical flops. Each flop is a list of three
    pokertools.Card objects.

    >>> len(get_all_canonicals())
    1755
    """
    all_possible_flops = combinations(CARDS.values(), r=3)
    return set([tuple(get_canonical(flop)) for flop in all_possible_flops])

#------------------------------------------------------------------------------
# Suit-Isomorphs


def get_suit_isomorphs(flop):
    """Returns a list of all suit-isomorphic combinations of the flop. Each
    flop is a list of three pokertools.Card objects.

    >>> flop = [CARDS['As'], CARDS['4s'], CARDS['Ts']]
    >>> for iso in get_suit_isomorphs(flop):
    ...     print(iso)
    [<Card: Ac>, <Card: 4c>, <Card: Tc>]
    [<Card: Ad>, <Card: 4d>, <Card: Td>]
    [<Card: Ah>, <Card: 4h>, <Card: Th>]
    [<Card: As>, <Card: 4s>, <Card: Ts>]

    >>> flop = [CARDS['Kd'], CARDS['Qh'], CARDS['8c']]
    >>> len(get_suit_isomorphs(flop))
    24
    """

    card1, card2, card3 = flop[0], flop[1], flop[2]

    if card1.suit == card2.suit == card3.suit:
        # For each suit, produce the suit pattern 'AAA'
        return [[CARDS[card1.rank + suit],        # <-- A
                 CARDS[card2.rank + suit],        # <-- A
                 CARDS[card3.rank + suit]]        # <-- A
                for suit in SUITS]

    elif card1.suit == card2.suit != card3.suit:
        # For each combination of two non-identical
        # suits, produce the suit pattern 'AAB'
        return [[CARDS[card1.rank + suit],        # <-- A
                 CARDS[card2.rank + suit],        # <-- A
                 CARDS[card3.rank + suit_2]]      # <-- B
                for suit in SUITS
                for suit_2 in SUITS
                if suit != suit_2]

    elif card1.suit != card2.suit == card3.suit:
        # For each combination of two non-identical
        # suits, produce the suit pattern 'ABB'
        return [[CARDS[card1.rank + suit],        # <-- A
                 CARDS[card2.rank + suit_2],      # <-- B
                 CARDS[card3.rank + suit_2]]      # <-- B
                for suit in SUITS
                for suit_2 in SUITS
                if suit != suit_2]

    elif card1.suit == card3.suit != card2.suit:
        # For each combination of two non-identical
        # suits, produce the suit pattern 'ABA'
        return [[CARDS[card1.rank + suit],        # <-- A
                 CARDS[card2.rank + suit_2],      # <-- B
                 CARDS[card3.rank + suit]]        # <-- A
                for suit in SUITS
                for suit_2 in SUITS
                if suit != suit_2]

    elif card1.suit != card2.suit != card3.suit:
        # For each combination of three non-identical
        # suits, produce the suit pattern 'ABC'
        return [[CARDS[card1.rank + suit],        # <-- A
                 CARDS[card2.rank + suit_2],      # <-- B
                 CARDS[card3.rank + suit_3]]      # <-- C
                for suit in SUITS
                for suit_2 in SUITS
                for suit_3 in SUITS
                if (suit != suit_2
                    and suit_2 != suit_3
                    and suit != suit_3)]

#------------------------------------------------------------------------------
# Translation Dict


def get_translation_dict(flop):
    """Returns a dict which maps suits to other suits. The keys represent the
    suits on the given flop. The values represent the suits on the canonical
    version. This tell us what the 'translation' is between them, allowing us
    to translate the suits of our holecards.

    >>> flop = [CARDS['6h'], CARDS['2d'], CARDS['Qd']]
    >>> get_canonical(flop)
    [<Card: 2c>, <Card: 6d>, <Card: Qc>]
    >>> get_translation_dict(flop) == {'c': 'h', 'd': 'c', 'h': 'd', 's': 's'}
    True
    """

    flop = sorted(flop)
    suit1, suit2, suit3 = (flop[0].suit, flop[1].suit, flop[2].suit)

    cano_flop = get_canonical(flop)
    cano_suit1, cano_suit2, cano_suit3 = (
        cano_flop[0].suit, cano_flop[1].suit, cano_flop[2].suit)

    # if the flop matches the canonical version, no translation necessary
    if (suit1, suit2, suit3) == (cano_suit1, cano_suit2, cano_suit3):
        return {'c': 'c', 'd': 'd', 'h': 'h', 's': 's'}

    unused = {'h', 'd', 'c', 's'} - {suit1, suit2, suit3}
    cano_unused = {'h', 'd', 'c', 's'} - {cano_suit1, cano_suit2, cano_suit3}
    both_unused = unused & cano_unused

    # listed for indexing the elements,
    # sorted for deterministic output
    unused = sorted(list(unused))
    cano_unused = sorted(list(cano_unused))
    both_unused = sorted(list(both_unused))

    if suit1 == suit2 == suit3:
        # suit pattern is 'AAA'
        return {
            suit1: cano_suit1,               # The first flop suit and the
            cano_suit1: suit1,               # first canon suit must switch.
            both_unused[0]: both_unused[0],  # The remaining two suits
            both_unused[1]: both_unused[1]   # don't matter
        }

    elif suit1 == suit2 != suit3:
        # suit pattern is 'AAB'
        return {
            suit1: cano_suit1,               # suit of 1st card = 1st canon
            suit3: cano_suit3,               # suit of 3rd card = 3rd canon
            unused[0]: cano_unused[0],       # Must be the remaining two
            unused[1]: cano_unused[1]        # suits of each set
        }

    elif suit1 != suit2 == suit3:
        # suit pattern is 'ABB'
        return {
            suit1: cano_suit1,               # suit of 1st card = 1st canon
            suit2: cano_suit2,               # suit of 2nd card = 2nd canon
            unused[0]: cano_unused[0],       # Must be the remaining two
            unused[1]: cano_unused[1]        # suits of each set
        }

    # Note the order of cards
    elif suit1 == suit3 != suit2:
        # suit pattern is 'ABA'
        return {
            suit1: cano_suit1,               # suit of 1st card = 1st canon
            suit2: cano_suit2,               # suit of 2nd card = 2nd canon
            unused[0]: cano_unused[0],       # Must be the remaining two
            unused[1]: cano_unused[1]        # suits of each set
        }

    elif suit1 != suit2 != suit3:
        # suit pattern is 'ABC'
        return {
            suit1: cano_suit1,               # suit of 1st card = 1st canon
            suit2: cano_suit2,               # suit of 2nd card = 2nd canon
            suit3: cano_suit3,               # suit of 3rd card = 3rd canon
            unused[0]: cano_unused[0]        # The remaining suits.
        }

#------------------------------------------------------------------------------
# doctests

__doc__ += """
>>> flop = [CARDS['6s'], CARDS['8d'], CARDS['7c']]
>>> get_canonical(flop)
[<Card: 6c>, <Card: 7d>, <Card: 8h>]
>>> get_translation_dict(flop) == {'c': 'd', 'd': 'h', 'h': 's', 's': 'c'}
True

>>> flop = [CARDS['Qs'], CARDS['Qd'], CARDS['4d']]
>>> get_canonical(flop)
[<Card: 4c>, <Card: Qc>, <Card: Qd>]
>>> get_translation_dict(flop) == {'c': 'h', 'd': 'c', 'h': 's', 's': 'd'}
True
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()
