from src.pypokertools.examples.isomorph import (
    get_all_canonicals,
    get_canonical,
    get_translation_dict,
    translate_holecards,
)
from src.pypokertools.pokertools import cards_from_str as flop
from src.pypokertools.pokertools import cards_from_str as holecards


def test_isomorph():
    assert len(get_all_canonicals()) == 1755

    assert get_canonical(flop('6s 8d 7c')) == flop('6c 7d 8h')
    assert get_translation_dict(flop('6s 8d 7c')) == {'c': 'd', 'd': 'h', 'h': 's', 's': 'c'}
    assert translate_holecards(flop('6s 8d 7c'), holecards('Ac 2s')) == holecards('Ad 2c')

    assert get_canonical(flop('Qs Qd 4d')) == flop('4c Qc Qd')
    assert get_translation_dict(flop('Qs Qd 4d')) == {'c': 'h', 'd': 'c', 'h': 's', 's': 'd'}
    assert translate_holecards(flop('Qs Qd 4d'), holecards('Ac 2s')) == holecards('Ah 2d')
