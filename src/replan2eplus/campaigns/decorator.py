from typing import NamedTuple, TypedDict
from dataclasses import dataclass
from itertools import product
from rich import print
from utils4plans.lists import chain_flatten


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
    def combinations(self):
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


def make_experimental_campaign(definitions: DefinitionDict):
    pass
