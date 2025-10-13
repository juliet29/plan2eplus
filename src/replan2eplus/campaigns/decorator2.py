from typing import Any, NamedTuple, TypedDict
from dataclasses import dataclass
from itertools import product
from rich import print
from utils4plans.lists import chain_flatten
from replan2eplus.examples.cases.minimal import test_rooms
from replan2eplus.examples.subsurfaces import e0, e1, e2, e3
from replan2eplus.ops.subsurfaces.interfaces import Dimension
from rich import print


class Option:
    def __init__(self, name, IS_DEFAULT=False) -> None:
        self.name: str = name
        self.IS_DEFAULT = IS_DEFAULT


class ModificationSelection(NamedTuple):
    name: str
    selection: str


class Variable(NamedTuple):
    name: str
    options: list[Option]

    def __post_init__(self):
        self.check_only_one_default_option()
        self.check_names_are_unique()

    def check_only_one_default_option(self):
        res = [i for i in self.options if i.IS_DEFAULT]
        assert len(res) == 1

    def check_names_are_unique(self):
        res = [i.name for i in self.options]
        assert len(set(res)) == len(res)

    @property
    def default_option(self):
        return [i.name for i in self.options if i.IS_DEFAULT][0]

    @property
    def non_default_options(self):
        return [i.name for i in self.options if not i.IS_DEFAULT]

    @property
    def non_default_selections(self):
        return [
            ModificationSelection(i, j)
            for i, j in product([self.name], self.non_default_options)
        ]


class ExperimentDef(NamedTuple):
    case_name: str
    modification: ModificationSelection | None = None


@dataclass
class DefinitionDict:
    case_names: list[str]
    case_variables: list[str]  # zones, surfaces
    modifications: list[Variable]

    @property
    def experiments(self):
        def define_mod_experiments(mod: Variable):
            return [
                ExperimentDef(i, j)
                for i, j in product(
                    self.case_names,
                    mod.non_default_selections,
                )
            ]

        default_cases = [ExperimentDef(i) for i in self.case_names]
        modification_cases = chain_flatten(
            [define_mod_experiments(mod) for mod in self.modifications]
        )

        return default_cases + modification_cases


@dataclass
class DataDict:
    case: dict[str, dict[str, list]]
    mods: dict[str, dict[str, Any]]  # really will be list

    def verify_match_defn_dict(self, defn_dict: DefinitionDict):
        assert set(self.case.keys()) == set(defn_dict.case_variables), (
            "Case Variables do not match"
        )
        # check case names  -> A, B, C
        # check modification variable name + options.. -> some typing here for sure..


def create_func_params(
    exp: ExperimentDef, data_dict: DataDict, defn_dict: DefinitionDict
):
    exp.case_name
    defn_dict.case_variables
    # dictionary is better than list here..
    case_values = {k: v[exp.case_name] for k, v in data_dict.case.items()}
    mod_values = {}
    # Actually this is the default behavior,
    for mod in defn_dict.modifications:
        default = mod.default_option
        mod_values[mod.name] = data_dict.mods[mod.name][default]
    if exp.modification:
        mod = exp.modification
        mod_values[mod.name] = data_dict.mods[mod.selection]
    # print(case_values)
    # print(mod_values)
    return case_values, mod_values
    # TODO some checks to make sure these are aligned


def make_experimental_campaign(defn_dict: DefinitionDict, data_dict: DataDict):
    def decorator_experimental_campaign(func):
        def wrapper(*args, **kwargs):
            experiments = defn_dict.experiments
            print("Have created experiments!")

            # case will be run multiple time for each experiment -
            case_values, mod_values = create_func_params(
                experiments[0], data_dict, defn_dict
            )

            case = func(**case_values, **mod_values)
            return

        return wrapper

    return decorator_experimental_campaign
