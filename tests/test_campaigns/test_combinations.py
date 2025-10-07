from replan2eplus.campaigns.decorator import DefinitionDict, Variable, Option
from itertools import product


class SampleDef:  # TOODO move to examples
    window_mods = Variable(
        "windows", [Option("-50%"), Option("standard", IS_DEFAULT=True), Option("+50%")]
    )

    door_open_modes = Variable(
        "interior door opening schedule",
        [
            Option("always closed"),
            Option("realistic opening"),
            Option("always open", IS_DEFAULT=True),
        ],
    )

    case_names = ["A", "B", "C"]
    case_variables = ["rooms", "connections"]

    @property
    def definition_dict(self):
        return DefinitionDict(
            self.case_names,
            self.case_variables,
            [self.window_mods, self.door_open_modes],
        )


def test_product():
    list1 = ["a", "b", "c"]
    list2 = [1, 2]
    res = list(product(list1, list2))
    assert res == [("a", 1), ("a", 2), ("b", 1), ("b", 2), ("c", 1), ("c", 2)]


def test_create_combinations():
    sample_def = SampleDef().definition_dict
    expected_number_of_combos = 15
    combos = sample_def.combinations
    assert len(combos) == expected_number_of_combos


if __name__ == "__main__":
    sample_def = SampleDef().definition_dict
    sample_def.combinations
