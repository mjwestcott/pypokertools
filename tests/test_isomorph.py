from examples.isomorph import (
    get_all_canonicals,
    get_canonical,
    get_translation_dict,
)
from pokertools import cards_from_str as flop


def test_isomorph():
    assert len(get_all_canonicals()) == 1755

    assert get_canonical(flop('6s 8d 7c')) == flop('6c 7d 8h')
    assert get_translation_dict(flop('6s 8d 7c')) == {'c': 'd', 'd': 'h', 'h': 's', 's': 'c'}

    assert get_canonical(flop('Qs Qd 4d')) == flop('4c Qc Qd')
    assert get_translation_dict(flop('Qs Qd 4d')) == {'c': 'h', 'd': 'c', 'h': 's', 's': 'd'}
