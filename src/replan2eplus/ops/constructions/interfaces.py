from dataclasses import dataclass
from utils4plans.lists import chain_flatten


@dataclass
class BaseConstructionSet:
    interior: str
    exterior: str


@dataclass
class EPConstructionSet:
    wall: BaseConstructionSet
    roof: BaseConstructionSet
    floor: BaseConstructionSet
    window: BaseConstructionSet
    door: BaseConstructionSet

    # TODO validate?

    @property
    def sets(self):
        return [self.wall, self.roof, self.floor, self.window, self.door]

    @property
    def names(self):
        return chain_flatten([[i.interior, i.exterior] for i in self.sets])
