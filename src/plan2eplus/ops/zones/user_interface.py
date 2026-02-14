from dataclasses import dataclass

from plan2eplus.geometry.contact_points import calculate_corner_points
from plan2eplus.geometry.domain import Domain
from plan2eplus.geometry.ortho_domain import OrthoDomain
from plan2eplus.ops.zones.idfobject import GeomeppyBlock


@dataclass
class Room:
    id: int
    name: str
    domain: Domain | OrthoDomain
    height: float
    reverse_coords: bool = False
    # TODO add default # notify that height is in meters!

    @property
    def coords(self):
        if isinstance(self.domain, Domain):
            corner_points = calculate_corner_points(self.domain)
            coords = corner_points.tuple_list
        else:
            coords = self.domain.tuple_list
        if self.reverse_coords:
            res = reversed(coords)
            return list(res)
        return coords

    # NOTE: this translation ensures that the domain is in the correct order, but should I have another check?

    @property
    def room_name(self):
        return f"`{self.name}`"

    @property
    def geomeppyupdated_block(self):
        return GeomeppyBlock(self.room_name, self.coords, self.height)

    # TODO -> geomeppyupdated expects points in a certain way by default, and need to confirm these are there..
    # TODO see normalize function in shapely
