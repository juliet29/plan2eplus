from dataclasses import dataclass

from plan2eplus.geometry.coords import Coord
from plan2eplus.geometry.plane import Plane
from plan2eplus.geometry.range import Range


@dataclass(frozen=True)
class Domain:
    horz_range: Range
    vert_range: Range
    plane: Plane | None = None

    def __str__(self) -> str:
        h = f"H{str(self.horz_range)}"
        v = f"V{str(self.horz_range)}"
        return f"{h}, {v}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Domain):
            r1 = self.horz_range == other.horz_range
            r2 = self.vert_range == other.vert_range
            r3 = self.plane == other.plane
            res = r1 and r2 and r3
            return res
        return False

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
