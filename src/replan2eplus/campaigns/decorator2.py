from typing import NamedTuple, TypedDict
from dataclasses import dataclass
from itertools import product
from rich import print
from utils4plans.lists import chain_flatten
from replan2eplus.examples.cases.minimal import test_rooms
from replan2eplus.examples.subsurfaces import e0, e1, e2, e3
from replan2eplus.ops.subsurfaces.interfaces import Dimension


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


def make_experimental_campaign(defn_dict: DefinitionDict):
    def decorator_experimental_campaign(func):
        def wrapper(*args, **kwargs):
            experiments = defn_dict.experiments
            # case will be run multiple time for each experiment -> # TODO write logic to pull from the data dict..
            print("Have created experiments!")
            data_dict = {
                "rooms": {
                    "A": [test_rooms[0], test_rooms[1]],
                    "B": [],
                },
                "edges": {
                    "A": {ix: i for ix, i in enumerate([e0, e1, e2, e3])},
                    "B": [],
                },
                "edge_detail_map": {"A": {0: [1, 2], 1: [3, 4]}}, # TODO think about how this is coming in.. is it coming in separetly -> is it the same for all? have that flexibility in any case.. 
                "windows": {"-50%": Dimension(0.5, 2), "standard": 1, "+50%": 2},
            }
            case = func(
                data_dict["rooms"]["A"],
                data_dict["edges"]["A"],
                data_dict["edge_detail_map"]["A"],
                data_dict["windows"]["-50%"],
            )
            return

        return wrapper

    return decorator_experimental_campaign
