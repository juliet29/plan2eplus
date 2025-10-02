from dataclasses import dataclass

from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.contact_points import calculate_corner_points
from replan2eplus.geometry.ortho_domain import OrthoDomain
from replan2eplus.idfobjects.zone import GeomeppyBlock
from typing import NamedTuple


@dataclass
class Room:
    id: int
    name: str
    domain: Domain | OrthoDomain
    height: float
    # TODO add default # notify that height is in meters!

    @property
    def coords(self):
        if isinstance(self.domain, Domain):
            corner_points = calculate_corner_points(self.domain)
            return corner_points.tuple_list
        else:
            return self.domain.tuple_list

    # NOTE: this translation ensures that the domain is in the correct order, but should I have another check?

    @property
    def room_name(self):
        return f"`{self.name}`"

    def geomeppy_block(self):
        return GeomeppyBlock(
            {
                "name": self.room_name,
                "coordinates": self.coords,
                "height": self.height,
            }
        )

    # TODO -> geomeppy expects points in a certain way by default, and need to confirm these are there..
    # TODO see normalize function in shapely
