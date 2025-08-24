from replan2eplus.ezobjects.base import EZObject
from dataclasses import dataclass
import replan2eplus.epnames.keys as epkeys
from typing import Protocol


@dataclass
class Construction(EZObject):
    expected_key: str = epkeys.CONSTRUCTION

    @property
    def construction_name(self):
        return self._epbunch.Name


@dataclass
class BaseConstructionSet:
    # default: Construction
    interior: str 
    exterior: str 

 

    # def __post_init__(self):
    #     if not self.interior:
    #         self.interior = self.default
    #     if not self.exterior:
    #         self.exterior = self.default


@dataclass
class EPConstructionSet:
    wall: BaseConstructionSet
    roof: BaseConstructionSet
    floor: BaseConstructionSet
    window: BaseConstructionSet
    door: BaseConstructionSet

    # TODO validate?