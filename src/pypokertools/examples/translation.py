"""
Translating PokerStove-style holecard notation to the 'individual cards'
notation used for holecards in pokertools.py.

In PokerStove notation (also used by PokerCruncher) Ace-King suited is
represented as AKs. Queen-Jack offsuit is QJo.

Simple examples:
    "66" -> ["6c 6d", "6c 6h", "6c 6s", "6d 6h", "6d 6s", "6c 6d"]
    "AKs" -> ["Ac Kc", "Ad Kd", "Ah Kh", "As Ks"]
    "QJo" -> ["Qc Jd", "Qd Jc", "Qh Jc", "Qs Jc",
              "Qc Jh", "Qd Jh", "Qh Jd", "Qs Jd",
              "Qc Js", "Qd Js", "Qh Js", "Qs Jh"]

The PokerStove format also includes range operators. For instance:
    "QQ+" -> ["Qc Qd", "Qc Qh", "Qc Qs", "Qd Qh", "Qd Qs", "Qc Qd",
              "Kc Kd", "Kc Kh", "Kc Ks", "Kd Kh", "Kd Ks", "Kc Kd",
              "Ac Ad", "Ac Ah", "Ac As", "Ad Ah", "Ad As", "Ac Ad"]
    "A5s-A3s" -> ["Ac 5c", "Ad 5d", "Ah 5h", "As 5s",
                  "Ac 4c", "Ad 4d", "Ah 4h", "As 4s",
                  "Ac 3c", "Ad 3d", "Ah 3h", "As 3s"]

Note: we will take position-isomorphs into account. "Ac Kc" is identical to
"Kc Ac" and we only want to to produce one of them. This will simplify and
reduce the space requirements of storing ranges of holecards.
"""
import re
from collections import namedtuple
from itertools import chain

from pypokertools.pokertools import (
    CANONICAL_HOLECARDS_NAMES,
    SUIT_COMBINATIONS,
    SUIT_PERMUTATIONS,
    SUITS,
    get_numerical_rank,
    get_string_rank,
    holecards,
)

#------------------------------------------------------------------------------
# Tokeniser


token_specification = [                                       # Examples:
    ("RANGE",        r"[2-9AKQJT]{2}(s|o)-[2-9AKQJT]{2}\2"),  # AKs-A2s
    ("RANGE_PAIR",   r"([2-9AKQJT])\4-([2-9AKQJT])\5"),       # 99-55
    ("PAIR",         r"([2-9AKQJT])\7\+?"),                   # 33
    ("SINGLE_COMBO", r"([2-9AKQJT][cdhs]){2}"),               # AhKh
    ("MULTI_COMBO",  r"[2-9AKQJT]{2}(s|o)\+?"),               # QJo
    ("SEPERATOR",    r"\s*,\s*"),
    ("CATCHALL",     r".+")
]
master_pat = re.compile("|".join("(?P<{}>{})".format(*pair) for pair in token_specification))


Token = namedtuple("Token", ["type", "value"])


class TokeniserError(Exception):
    pass


def generate_tokens(pattern, text):
    scanner = pattern.scanner(text)
    for m in iter(scanner.match, None):
        token = Token(m.lastgroup, m.group())
        yield token


def canonise(holecards):
    """
    Takes a single pair of cards and returns the canonical representation of
    that pair according to CANONICAL_HOLECARDS_NAMES
    """
    if holecards in CANONICAL_HOLECARDS_NAMES:
        return holecards
    else:
        return "{} {}".format(holecards[3:5], holecards[0:2])


def process_one_name(stove_name):
    """
    Translates a single PokerStove-style name of holecards into an
    expanded list of pokertools-style names.

    For example:
        "AKs" -> ["Ac Kc", "Ad Kd", "Ah Kh", "As Ks"]
        "66" -> ["6c 6d", "6c 6h", "6c 6s", "6d 6h", "6d 6s", "6c 6d"]
    """
    if len(stove_name) == 3:
        rank1, rank2, suit_mark = stove_name
        if suit_mark == "s":
            return [
                "{}{} {}{}".format(rank1, suit, rank2, suit)
                for suit in SUITS
            ]
        elif suit_mark == "o":
            return [
                "{}{} {}{}".format(rank1, suit1, rank2, suit2)
                for suit1, suit2 in SUIT_PERMUTATIONS
            ]
        else:
            raise TokeniserError("incorrect suit_mark in stove_name: {}".format(stove_name))
    else:
        rank1, rank2 = stove_name
        if rank1 == rank2:
            return [
                "{}{} {}{}".format(rank1, suit1, rank2, suit2)
                for suit1, suit2 in SUIT_COMBINATIONS
            ]
        else:
            raise TokeniserError("rank1 != rank2 in stove_name: {}".format(stove_name))


def process_one_token(token):
    """
    Translates any given single token. For example:
        "77-55" -> ["7c 7d", "7c 7h", "7c 7s", "7d 7h", "7d 7s", "7c 7d",
                    "6c 6d", "6c 6h", "6c 6s", "6d 6h", "6d 6s", "6c 6d",
                    "5c 5d", "5c 5h", "5c 5s", "5d 5h", "5d 5s", "5c 5d"]
    """
    # Let's say token.value is "A5s-A2s". Our naming convention is this:
    #   'A' is the 'const_rank'
    #   '5' is the 'high_rank'
    #   '2' is the 'low_rank'
    #   's' is the 'suit_mark'

    if token.type == "RANGE":
        const_rank, high_rank, low_rank, suit_mark = token.value[0], token.value[1], token.value[5], token.value[2]
        high = get_numerical_rank(high_rank)
        low = get_numerical_rank(low_rank)
        # Produce a list such as ["A5s", "A4s", "A3s", "A2s"] for processing
        names = [
            "{}{}{}".format(const_rank, get_string_rank(i), suit_mark)
            for i in range(high, (low - 1), -1)
        ]
        return list(chain.from_iterable(process_one_name(name) for name in names))

    elif token.type == "RANGE_PAIR":
        high_rank, low_rank = token.value[1], token.value[3]
        high = get_numerical_rank(high_rank)
        low = get_numerical_rank(low_rank)
        # Produce a list such as ["77", "66", "55"] for processing
        names = [
            get_string_rank(i) * 2
            for i in range(high, (low - 1), -1)
        ]
        return list(chain.from_iterable(process_one_name(name) for name in names))

    elif token.type == "PAIR":
        if token.value.endswith("+"):
            # '55+' is equivalent to 'AA-55'
            return process_one_token(Token("RANGE_PAIR", "AA" + "-" + token.value[0:2]))
        else:
            return process_one_name(token.value)

    elif token.type == "SINGLE_COMBO":
        card1, card2 = token.value[0:2], token.value[2:4]
        return ["{} {}".format(card1, card2)]

    elif token.type == "MULTI_COMBO":
        if token.value.endswith("+"):
            # 'Q2s+' is equivalent to 'QJs-Q2s'
            const_rank, low_rank, suit_mark = token.value[0], token.value[1], token.value[2]
            const = get_numerical_rank(const_rank)
            high_rank = get_string_rank(const - 1)
            new_token = Token("RANGE", "{}{}{}-{}{}{}".format(
                const_rank, high_rank, suit_mark,
                const_rank, low_rank, suit_mark
            ))
            return process_one_token(new_token)
        else:
            return process_one_name(token.value)

    else:
        raise TokeniserError("unexpected token: {}".format(token))


def translate(text):
    """
    Translates a string of PokerStove-style names of holecards into the
    corresponding string of names from CANONICAL_HOLECARDS_NAMES.

    >>> stove_string = "JJ+, 66-22, A5s-A2s, Q9s+, J9s+, 8d7d, ATo+, KTo+"
    >>> len(list(translate(stove_string)))
    175
    """
    tokens = list(generate_tokens(master_pat, text))
    errors = [t for t in tokens if t.type == "CATCHALL"]
    if errors:
        raise TokeniserError("unexpected tokens: {}".format(errors))
    for token in tokens:
        if token.type != "SEPERATOR":
            yield from (canonise(name) for name in process_one_token(token))


def to_cards(text):
    return [holecards(name) for name in translate(text)]
