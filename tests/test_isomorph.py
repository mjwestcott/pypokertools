from pokertools import cards_from_str
from examples.isomorph import get_canonical, get_all_canonicals, get_translation_dict


def test_isomorph():
    assert len(get_all_canonicals()) == 1755

    flop = cards_from_str('6s 8d 7c')
    assert get_canonical(flop) == cards_from_str('6c 7d 8h')
    assert get_translation_dict(flop) == {'c': 'd', 'd': 'h', 'h': 's', 's': 'c'}

    flop = cards_from_str('Qs Qd 4d')
    assert get_canonical(flop) == cards_from_str('4c Qc Qd')
    assert get_translation_dict(flop) == {'c': 'h', 'd': 'c', 'h': 's', 's': 'd'}
