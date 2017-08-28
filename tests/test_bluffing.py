from pokertools import CARDS, HOLECARDS, cards_from_str
from examples.bluffing import (
    is_onepair,
    is_3straight,
    is_3flush,
    is_bluffcandidate,
    get_bluffcandidates,
)

hand = flop = holecards = cards_from_str


def test_is_onepair():
    assert is_onepair(holecards('2c 4h'), flop('Tc Th 5d'), required_holecards=0)
    assert is_onepair(holecards('2c Th'), flop('Tc 4h 5d'), required_holecards=1)
    assert is_onepair(holecards('2c 2h'), flop('Ac Kh Qd'), required_holecards=2)
    assert not is_onepair(holecards('2c 4h'), flop('5c Jh Qd'), required_holecards=0)
    assert not is_onepair(holecards('4c Ah'), flop('5c 5h Qd'), required_holecards=1)
    assert not is_onepair(holecards('2c 4c'), flop('5c 5h Qd'), required_holecards=2)


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
        holecards('Kc Qc'),
        holecards('6c 5c'),
    }

    assert set(get_bluffcandidates(flop('6s 6d Kc'))) == {
        holecards('Qd Jd'),
        holecards('Qc Jc'),
        holecards('Qs Js'),
        holecards('8s 7s'),
        holecards('8c 7c'),
        holecards('8d 7d'),
        holecards('5d 4d'),
        holecards('5c 4c'),
        holecards('5s 4s'),
        holecards('Ad Qd'),
        holecards('Ac Qc'),
        holecards('As Qs'),
    }

    # TODO: This hand exists in the bluff candidate set, but actually
    # it's an open-ended straight draw which makes it a semi-bluff.
    assert holecards('6c 5c') in set(get_bluffcandidates(flop('4s 7s Ac')))
