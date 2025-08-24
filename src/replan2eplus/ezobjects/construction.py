from replan2eplus.ezobjects.base import EZObject
from dataclasses import dataclass
import replan2eplus.epnames.keys as epkeys


@dataclass
class Construction(EZObject):
    expected_key: str = epkeys.CONSTRUCTION


# @dataclass
# class BaseConstructionSet:
#     default: Construction
#     interior: Construction | None = None
#     exterior: Construction | None = None

#     def __post_init__(self):
#         if not self.interior:
#             self.interior = self.default
#         if not self.exterior:
#             self.exterior = self.default

# @dataclass
# class EPConstructionSet:
#     wall: BaseConstructionSet
#     roof: BaseConstructionSet
#     floor: BaseConstructionSet
#     window: BaseConstructionSet
#     door: BaseConstructionSet
