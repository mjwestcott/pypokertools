from pokertools import CARDS, HOLECARDS, cards_from_str
from examples.bluffing import (
    is_3straight,
    is_3flush,
    is_bluffcandidate,
    get_bluffcandidates,
)

hand = flop = cards_from_str
holecards = HOLECARDS.__getitem__


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

    # TODO: This returns no candidates because our hand has a pair.
    # We should ignore pairs made without our holecards.
    assert set(get_bluffcandidates(flop('2s 2s Ac'))) == set()

    # TODO: This hand exists in the bluff candidate set, but actually
    # it's an open-ended straight draw which makes it a semi-bluff.
    assert holecards('6c 5c') in set(get_bluffcandidates(flop('4s 7s Ac')))
