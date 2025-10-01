from dataclasses import dataclass

from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.geometry.domain import Domain
from replan2eplus.idfobjects.zone import GeomeppyBlock
from typing import NamedTuple


@dataclass
class Room:
    id: int
    name: str
    domain: Domain
    height: float
    # TODO add default # notify that height is in meters!

    @property
    def coords(self):
        return self.domain.corner.tuple_list  # NOTE: this translation ensures that the domain is in the correct order, but should I have another check?

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


