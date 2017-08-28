from pokertools import cards_from_str
from examples.flops import (
    is_rainbow,
    is_monotone,
    has_pair,
    has_threeofakind,
    has_3straight,
    has_2flush,
    has_gutshot,
)

flop = cards_from_str


def test_is_rainbow():
    assert is_rainbow(flop('Ah Td 3c'))
    assert is_rainbow(flop('Ah Ks 3c'))
    assert is_rainbow(flop('Ah Td 3s'))
    assert not is_rainbow(flop('Kd 5d 2d'))
    assert not is_rainbow(flop('Kd 8d 6s'))
    assert not is_rainbow(flop('Ks Qh 2s'))


def test_is_monotone():
    assert is_monotone(flop('Ah Th 3h'))
    assert is_monotone(flop('Ac Tc 3c'))
    assert is_monotone(flop('Ks Qs 2s'))
    assert not is_monotone(flop('Ah Td 3c'))
    assert not is_monotone(flop('As Ts 3d'))
    assert not is_monotone(flop('Ks Qd 2s'))


def test_has_pair():
    assert has_pair(flop('Ah Ad 3c'))
    assert has_pair(flop('Ah 3d 3c'))
    assert has_pair(flop('Th Td 3c'))
    assert not has_pair(flop('Ah Td 3c'))
    assert not has_pair(flop('As Ts 3s'))
    assert not has_pair(flop('Ks Qd 2s'))


def test_has_threeofakind():
    assert has_threeofakind(flop('Ah Ad Ac'))
    assert has_threeofakind(flop('Th Td Tc'))
    assert has_threeofakind(flop('3h 3d 3c'))
    assert not has_threeofakind(flop('Ah Td 3c'))
    assert not has_threeofakind(flop('As Ts 3s'))
    assert not has_threeofakind(flop('Ks Qd 2s'))


def test_has_3straight():
    assert has_3straight(flop('Ah 2d 3c'))
    assert has_3straight(flop('Jh Td 9c'))
    assert has_3straight(flop('Ks Qd Js'))
    assert not has_3straight(flop('Ah Td 3c'))
    assert not has_3straight(flop('As Ts 3s'))
    assert not has_3straight(flop('Ts 9s 7c'))


def test_has_gutshot():
    assert has_gutshot(flop('Ts 9s 7c'))
    assert has_gutshot(flop('Ah 2d 4c'))
    assert has_gutshot(flop('Ah 3d 4c'))
    assert not has_gutshot(flop('Ah Td 3c'))
    assert not has_gutshot(flop('As Ts 3s'))
    assert not has_gutshot(flop('Ts 9s 8c'))


def test_has_2flush():
    assert has_2flush(flop('Ah Th 3c'))
    assert has_2flush(flop('Ah Td 3d'))
    assert has_2flush(flop('Ks Qd 2s'))
    assert not has_2flush(flop('Ah Th 3h'))
    assert not has_2flush(flop('Ah Td 3c'))
    assert not has_2flush(flop('Ks Td Th'))
