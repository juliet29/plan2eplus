from dataclasses import dataclass
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.planedef import Plane
from replan2eplus.geometry.range import Range


@dataclass(frozen=True)
class Domain:
    horz_range: Range
    vert_range: Range
    plane: Plane | None = None

    @property
    def area(self):
        return self.horz_range.size * self.vert_range.size

    @property
    def aspect_ratio(self):
        return self.horz_range.size / self.vert_range.size

    @property
    def centroid(self):
        return Coord(self.horz_range.midpoint, self.vert_range.midpoint)

    # @property
    # def nonant(self):
    #     return Nonant(self.horz_range.trirange, self.vert_range.trirange)
