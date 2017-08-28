import pytest

from pokertools import flop, holecards, ConflictingCards
from properties.complex import (
    is_onepair,
    is_3straight,
    is_3flush,
    has_two_overcards,
)


def test_five_cards_decorator():
    with pytest.raises(ConflictingCards):
        is_onepair(holecards('Ac Ac'), flop('Tc Th 5d'))

    with pytest.raises(ConflictingCards):
        is_3straight(holecards('Ac Tc'), flop('Tc Th 5d'))

    with pytest.raises(ConflictingCards):
        is_3flush(holecards('Ac 5d'), flop('Tc Th 5d'))

    with pytest.raises(ValueError):
        is_onepair(holecards('Ac'), flop('Tc Th 5d'))


def test_has_two_overcards():
    assert has_two_overcards(holecards('Kh Ts'), flop('4c 3h 2d'))
    assert has_two_overcards(holecards('Ac Kc'), flop('Tc Th 5d'))  # Even though pair on board
    assert has_two_overcards(holecards('Qd Qc'), flop('Tc 4h 5d'))  # Even though it's a pair
    assert not has_two_overcards(holecards('Ac 4h'), flop('5c 5h Qd'))
    assert not has_two_overcards(holecards('Kh Ts'), flop('Qd Qc Qs'))


def test_is_onepair():
    assert is_onepair(holecards('2c 4h'), flop('Tc Th 5d'), exclude_board=False)
    assert is_onepair(holecards('2c Th'), flop('Tc 4h 5d'), exclude_board=False)
    assert is_onepair(holecards('2c 2h'), flop('Ac Kh Qd'), exclude_board=True)
    assert is_onepair(holecards('2c Qh'), flop('Ac Kh Qd'), exclude_board=True)
    assert not is_onepair(holecards('2c 4h'), flop('5c Jh Qd'), exclude_board=False)
    assert not is_onepair(holecards('4c Ah'), flop('5c 5h Qd'), exclude_board=True)


def test_is_3straight():
    assert is_3straight(holecards('2c 4h'), flop('Tc Jh Qd'), required_holecards=0)
    assert is_3straight(holecards('2c Th'), flop('3c Jh Qd'), required_holecards=1)
    assert is_3straight(holecards('2c 3h'), flop('4c Jh Qd'), required_holecards=2)
    assert not is_3straight(holecards('2c 4h'), flop('5c Jh Qd'), required_holecards=0)
    assert not is_3straight(holecards('2c 4h'), flop('5c Jh Qd'), required_holecards=1)
    assert not is_3straight(holecards('2c 4c'), flop('5c Jh Ad'), required_holecards=2)


def test_is_3flush():
    assert is_3flush(holecards('2c 4h'), flop('Td Jd Qd'), required_holecards=0)
    assert is_3flush(holecards('2c Th'), flop('3h Jh Qd'), required_holecards=1)
    assert is_3flush(holecards('2d 4d'), flop('5d Jh Qh'), required_holecards=2)
    assert not is_3flush(holecards('2c 4c'), flop('Ts Jh Qd'), required_holecards=0)
    assert not is_3flush(holecards('2c Th'), flop('3c Jh Qd'), required_holecards=1)
    assert not is_3flush(holecards('2c 4c'), flop('5s Jh Qd'), required_holecards=2)
