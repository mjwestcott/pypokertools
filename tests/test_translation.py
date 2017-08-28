from examples.translation import process_whole_string


def test_translation():
    assert set(process_whole_string("66")) == {
        "6c 6d", "6c 6h", "6c 6s", "6d 6h", "6d 6s", "6h 6s"
    }
    assert set(process_whole_string("AKs")) == {
        "Ac Kc", "Ad Kd", "Ah Kh", "As Ks"
    }
    assert set(process_whole_string("QJo")) == {
        "Qc Jd", "Qd Jc", "Qh Jc", "Qs Jc",
        "Qc Jh", "Qd Jh", "Qh Jd", "Qs Jd",
        "Qc Js", "Qd Js", "Qh Js", "Qs Jh",
    }
    assert set(process_whole_string("QQ+")) == {
        "Qc Qd", "Qc Qh", "Qc Qs", "Qd Qh", "Qd Qs", "Qh Qs",
        "Kc Kd", "Kc Kh", "Kc Ks", "Kd Kh", "Kd Ks", "Kh Ks",
        "Ac Ad", "Ac Ah", "Ac As", "Ad Ah", "Ad As", "Ah As",
    }
    assert set(process_whole_string("A5s-A3s")) == {
        "Ac 5c", "Ad 5d", "Ah 5h", "As 5s",
        "Ac 4c", "Ad 4d", "Ah 4h", "As 4s",
        "Ac 3c", "Ad 3d", "Ah 3h", "As 3s",
    }
    button_opening_range = (
        "22+, A2s+, K2s+, Q2s+, J6s+, T6s+, 96s+, 86s+, 75s+, 64s+, "
        "54s, A2o+, K9o+, Q9o+, J9o+, T8o+, 98o, 87o"
    )
    result = process_whole_string(button_opening_range)
    assert len(result) == 586
