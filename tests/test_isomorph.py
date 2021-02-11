from src.pypokertools.examples.isomorph import (
    get_all_canonicals,
    get_canonical,
    get_translation_dict,
    translate_holecards,
    translate_board,
)
from src.pypokertools.pokertools import cards_from_str as flop
from src.pypokertools.pokertools import cards_from_str as board
from src.pypokertools.pokertools import cards_from_str as holecards


def test_isomorph():
    assert len(get_all_canonicals()) == 1755

    assert get_canonical(flop('6s 8d 7c')) == flop('6c 7d 8h')
    assert get_translation_dict(flop('6s 8d 7c')) == {'c': 'd', 'd': 'h', 'h': 's', 's': 'c'}
    assert translate_holecards(flop('6s 8d 7c'), holecards('Ac 2s')) == holecards('Ad 2c')
    assert translate_board(board('6s 8d 7c Ah Ks')) == board('6c 8h 7d As Kc')

    assert get_canonical(flop('Qs Qd 4d')) == flop('4c Qc Qd')
    assert get_translation_dict(flop('Qs Qd 4d')) == {'c': 'h', 'd': 'c', 'h': 's', 's': 'd'}
    assert translate_holecards(flop('Qs Qd 4d'), holecards('Ac 2s')) == holecards('Ah 2d')
    assert translate_board(board('Qs Qd 4d 3s')) == board('Qd Qc 4c 3d')

    assert get_canonical(flop('Kc 2h 2c')) == flop('2c 2d Kc')
    assert get_translation_dict(flop('Kc 2h 2c')) == {'c': 'c', 'd': 'h', 'h': 'd', 's': 's'}
    assert translate_holecards(flop('Kc 2h 2c'), holecards('Ac 9s')) == holecards('Ac 9s')
    assert translate_board(board('Kc 2h 2c Kh 3d')) == board('Kc 2d 2c Kd 3h')
    
    assert get_canonical(flop('5s 8h As')) == flop('5c 8d Ac')
    assert get_translation_dict(flop('5s 8h As')) == {'c': 'h', 'd': 's', 'h': 'd', 's': 'c'}
    assert translate_holecards(flop('5s 8h As'), holecards('Ac Jc')) == holecards('Ah Jh')
    assert translate_board(board('5s 8h As 2h Th')) == board('5c 8d Ac 2d Td')
