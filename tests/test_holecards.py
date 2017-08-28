from pokertools import cards_from_str
from examples.holecards import (
    is_pair,
    is_suited,
    is_connected,
    has_one_gap,
    has_two_gap,
)

holecards = cards_from_str


def test_is_pair():
    assert is_pair(holecards('Ad Ac'))
    assert is_pair(holecards('Ts Td'))
    assert is_pair(holecards('2c 2d'))
    assert not is_pair(holecards('Ks Qs'))
    assert not is_pair(holecards('Ac 2d'))
    assert not is_pair(holecards('Td 9d'))


def test_is_suited():
    assert is_suited(holecards('Ad Kd'))
    assert is_suited(holecards('Ad 2d'))
    assert is_suited(holecards('Ts 9s'))
    assert not is_suited(holecards('Ad Kc'))
    assert not is_suited(holecards('Ah 2s'))
    assert not is_suited(holecards('Tc 9h'))


def test_is_connected():
    assert is_connected(holecards('Ad 2c'))
    assert is_connected(holecards('Ad Kc'))
    assert is_connected(holecards('Jh Th'))
    assert not is_connected(holecards('Ad Qc'))
    assert not is_connected(holecards('4h 2h'))
    assert not is_connected(holecards('Jc 9c'))


def test_has_one_gap():
    assert has_one_gap(holecards('Ad Qd'))
    assert has_one_gap(holecards('Ad 3c'))
    assert has_one_gap(holecards('Ts 8h'))
    assert not has_one_gap(holecards('Ad Kd'))
    assert not has_one_gap(holecards('Ad 2c'))
    assert not has_one_gap(holecards('Ts 9h'))


def test_has_two_gap():
    assert has_two_gap(holecards('Ad Jd'))
    assert has_two_gap(holecards('Ad 4c'))
    assert has_two_gap(holecards('Ts 7h'))
    assert not has_two_gap(holecards('Ad Qd'))
    assert not has_two_gap(holecards('Ad 3c'))
    assert not has_two_gap(holecards('Ts 8h'))
