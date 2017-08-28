from pokertools import hand, flop, holecards
from properties.hand import (
    is_straightflush,
    is_fourofakind,
    is_fullhouse,
    is_flush,
    is_straight,
    is_threeofakind,
    is_twopair,
    is_onepair,
    is_nopair,
    is_pair_or_better,
    is_twopair_or_better,
)
from properties.flop import (
    is_rainbow,
    is_monotone,
    has_pair,
    has_threeofakind,
    has_3straight,
    has_2flush,
    has_gutshot,
)
from properties.holecards import(
    is_pair,
    is_suited,
    is_connected,
    has_one_gap,
    has_two_gap,
)


#------------------------------------------------------------------------------
# Hand properties


def test_is_straightflush():
    assert is_straightflush(hand('4h 5h 6h 7h 8h'))
    assert is_straightflush(hand('As Ks Qs Js Ts'))
    assert not is_straightflush(hand('4c 5h 6h 7h 8h'))
    assert not is_straightflush(hand('Ad Ks Qs Js Ts'))


def test_is_fourofakind():
    assert is_fourofakind(hand('4h 4d 4s 4c Ac'))
    assert is_fourofakind(hand('Ac As Ah Ad 2d'))
    assert not is_fourofakind(hand('4c 5h 6h 7h 8h'))
    assert not is_fourofakind(hand('Ad Ks Qs Js Ts'))


def test_is_fullhouse():
    assert is_fullhouse(hand('4h 4d 4s 5h 5d'))
    assert is_fullhouse(hand('Ac As Ah 2c 2s'))
    assert not is_fullhouse(hand('4h 4d 4s 7h 8h'))
    assert not is_fullhouse(hand('Ad As Ah 2c Kd'))


def test_is_flush():
    assert is_flush(hand('4d 5d 8d Jd Qd'))
    assert is_flush(hand('Ac 8c 7c 5c 2c'))
    assert not is_flush(hand('4h 4s 5s 7s 8s'))
    assert not is_flush(hand('Ad 7d 6d 3d 2h'))


def test_is_straight():
    assert is_straight(hand('4h 5d 6s 7h 8d'))
    assert is_straight(hand('Ac 2s 3h 4c 5s'))
    assert is_straight(hand('Tc Js Qh Kc As'))
    assert not is_straight(hand('4h 5d 6s 7h 9h'))
    assert not is_straight(hand('Ad 2s 3h 4c 6d'))


def test_is_threeofakind():
    assert is_threeofakind(hand('4h 4d 4s 5h 6d'))
    assert is_threeofakind(hand('Ac As Ah 2c Ks'))
    assert not is_threeofakind(hand('4h 4d 7s 7h 8h'))
    assert not is_threeofakind(hand('Ad 2s 3s 4s 5s'))


def test_is_twopair():
    assert is_twopair(hand('4h 4d 5s 5h 6d'))
    assert is_twopair(hand('Ac As 2h 2c Ks'))
    assert not is_twopair(hand('4h 4d 5s 7h 8h'))
    assert not is_twopair(hand('Ad As 2h Qc Kd'))


def test_is_onepair():
    assert is_onepair(hand('4h 4d 5s 6h 7d'))
    assert is_onepair(hand('Ac As 2h Qc Ks'))
    assert not is_onepair(hand('4h 4d 4s 7h 8h'))
    assert not is_onepair(hand('Ad 2s 3h 4c 6d'))


def test_is_nopair():
    assert is_nopair(hand('4h 7d 9s Jh Ad'))
    assert is_nopair(hand('Ac 2s 3h 4c 6s'))
    assert not is_nopair(hand('4h 4d 4s 7h 8h'))
    assert not is_nopair(hand('As Ks Qs Js Ts'))


def test_is_pair_or_better():
    assert is_pair_or_better(hand('Ad Ac 7s 6s 5s'))
    assert is_pair_or_better(hand('Ad Ac Kd Kc 2h'))
    assert is_pair_or_better(hand('Ad Ac As 6c 5c'))
    assert is_pair_or_better(hand('Ad Kh Qs Jc Td'))
    assert is_pair_or_better(hand('Ad 8d 7d 6d 5d'))
    assert is_pair_or_better(hand('Ad Ac As 5d 5c'))
    assert is_pair_or_better(hand('Ad Ac As Ah 5c'))
    assert is_pair_or_better(hand('Ad Kd Qd Jd Td'))
    assert not is_pair_or_better(hand('Ad Kd Qd Jd 3c'))
    assert not is_pair_or_better(hand('Ts 9s 7c 6s 5s'))


def test_is_twopair_or_better():
    assert is_twopair_or_better(hand('Ad Ac Kd Kc 2h'))
    assert is_twopair_or_better(hand('Ad Ac As 6c 5c'))
    assert is_twopair_or_better(hand('Ad Kh Qs Jc Td'))
    assert is_twopair_or_better(hand('Ad 8d 7d 6d 5d'))
    assert is_twopair_or_better(hand('Ad Ac As 5d 5c'))
    assert is_twopair_or_better(hand('Ad Ac As Ah 5c'))
    assert is_twopair_or_better(hand('Ad Kd Qd Jd Td'))
    assert not is_twopair_or_better(hand('Ad Ac 7s 6s 5s'))
    assert not is_twopair_or_better(hand('Ad Kd Qd Jd 3c'))
    assert not is_twopair_or_better(hand('Ts 9s 7c 6s 5s'))


#------------------------------------------------------------------------------
# Flop properties


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

#------------------------------------------------------------------------------
# Holecards properties


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
