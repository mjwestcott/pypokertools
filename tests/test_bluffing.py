from pokertools import flop, holecards
from examples.bluffing import (
    is_bluffcandidate,
    get_bluffcandidates,
)


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


def test_is_bluffcandidate():
    assert is_bluffcandidate(holecards('2c 3c'), flop('4c Jh Qd'))
    assert is_bluffcandidate(holecards('9h Th'), flop('3c Jh Qd'))
    assert is_bluffcandidate(holecards('Ac 3c'), flop('2c Jh Qd'))
    assert not is_bluffcandidate(holecards('2c 4h'), flop('Tc Jh Qd'))
    assert not is_bluffcandidate(holecards('2c Th'), flop('3c Jh Ad'))
    assert not is_bluffcandidate(holecards('Ac 3c'), flop('2c Jh Ad'))  # It's a pair
