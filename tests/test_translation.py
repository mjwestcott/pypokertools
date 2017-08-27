from examples.translation import process_whole_string


def test_translation():
    button_opening_range = (
        "22+, A2s+, K2s+, Q2s+, J6s+, T6s+, 96s+, 86s+, 75s+, 64s+, "
        "54s, A2o+, K9o+, Q9o+, J9o+, T8o+, 98o, 87o"
    )
    result = process_whole_string(button_opening_range)
    assert len(result) == 586
