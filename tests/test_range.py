from replan2eplus.geometry.range import Range, expand_range

FACTOR = 1.5


def test_expand_range():
    base = Range(1, 3)
    new_range = expand_range(base, FACTOR)
    expected_range = Range(0.5, 3.5)
    assert new_range == expected_range


def test_expand_range_with_neg():
    base = Range(-1, 1)
    new_range = expand_range(base, FACTOR)
    expected_range = Range(-1.5, 1.5)
    assert new_range == expected_range
