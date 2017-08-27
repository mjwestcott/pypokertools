from pokertools import (
    CARDS,
    CARD_NAMES,
    HOLECARDS,
    HOLECARDS_NAMES,
    make_deck,
    deal,
)


def test_pokertools():
    assert len(CARDS) == len(CARD_NAMES) == 52
    assert len(HOLECARDS) == len(HOLECARDS_NAMES) == 2652

    seven_clubs = CARDS['7c']
    assert seven_clubs.name == '7c'
    assert seven_clubs.suit == 'c'
    assert seven_clubs.rank == '7'
    assert seven_clubs.numerical_rank == 7

    ace_hearts = CARDS['Ah']
    assert ace_hearts.name == 'Ah'
    assert ace_hearts.suit == 'h'
    assert ace_hearts.rank == 'A'
    assert ace_hearts.numerical_rank == 14

    assert CARDS['Ks'] > CARDS['Qh']
    assert CARDS['2d'] <= CARDS['3d']

    Ah7c = HOLECARDS['Ah 7c']
    assert Ah7c[0] == ace_hearts
    assert Ah7c[1] == seven_clubs

    deck = make_deck()
    assert len(deck) == 52

    holecards = deal(deck, n=2)
    assert len(holecards) == 2
    assert len(deck) == 50

    flop = deal(deck, n=3)
    assert len(flop) == 3
    assert len(deck) == 47
