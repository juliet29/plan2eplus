from itertools import product

from replan2eplus.examples.campaigns import SampleDef


def test_product():
    list1 = ["a", "b", "c"]
    list2 = [1, 2]
    res = list(product(list1, list2))
    assert res == [("a", 1), ("a", 2), ("b", 1), ("b", 2), ("c", 1), ("c", 2)]


def test_create_combinations():
    sample_def = SampleDef().definition_dict
    expected_number_of_combos = 15
    combos = sample_def.experiments
    assert len(combos) == expected_number_of_combos


if __name__ == "__main__":
    sample_def = SampleDef().definition_dict
    sample_def.experiments
