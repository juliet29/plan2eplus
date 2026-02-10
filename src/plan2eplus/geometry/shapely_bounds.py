from plan2eplus.geometry.domain import Domain
from plan2eplus.geometry.range import Range


from typing import NamedTuple


class ShapelyBounds(NamedTuple):
    minx: float
    miny: float
    maxx: float
    maxy: float

    @property
    def domain(self):
        horz_range = Range(self.minx, self.maxx)
        vert_range = Range(self.miny, self.maxy)
        return Domain(horz_range, vert_range)
