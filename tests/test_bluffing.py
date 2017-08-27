from pokertools import CARDS, HOLECARDS, cards_from_str
from examples.bluffing import (
    is_straightflush,
    is_fourofakind,
    is_fullhouse,
    is_flush,
    is_straight,
    is_threeofakind,
    is_twopair,
    is_onepair,
    is_nopair,
    is_3straight,
    is_3flush,
    is_bluffcandidate,
    get_bluffcandidates,
)

hand = flop = cards_from_str
holecards = HOLECARDS.get


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


def test_is_bluffcandidate():
    assert is_bluffcandidate(holecards('2c 3c'), flop('4c Jh Qd'))
    assert is_bluffcandidate(holecards('9h Th'), flop('3c Jh Qd'))
    assert is_bluffcandidate(holecards('Ac 3c'), flop('2c Jh Qd'))
    assert not is_bluffcandidate(holecards('2c 4h'), flop('Tc Jh Qd'))
    assert not is_bluffcandidate(holecards('2c Th'), flop('3c Jh Ad'))
    assert not is_bluffcandidate(holecards('Ac 3c'), flop('2c Jh Ad'))  # It's a pair


def test_get_bluffcandidates():
    assert set(get_bluffcandidates(flop('2s 4s Ac'))) == {
        holecards('Qc Kc'),
        holecards('5c 6c'),
    }

    # TODO: This returns no candidates because our hand has a pair.
    # We should ignore pairs made without our holecards.
    assert set(get_bluffcandidates(flop('2s 2s Ac'))) == set()

    # TODO: This hand exists in the bluff candidate set, but actually
    # it's an open-ended straight draw which makes it a semi-bluff.
    assert holecards('5c 6c') in set(get_bluffcandidates(flop('4s 7s Ac')))
