from dataclasses import dataclass
from typing import NamedTuple


class MaterialInput(NamedTuple):
    name: str
    key: str

    def material_properties(self):
        if self.key == "":
            expected_properties = {}

    # TODO this will have inheritance -> there are many types of materials!




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
