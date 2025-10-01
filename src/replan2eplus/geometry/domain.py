from dataclasses import dataclass
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.nonant import Nonant
from typing import Literal, NamedTuple
from replan2eplus.geometry.range import Range

import numpy as np


AXIS = Literal["X", "Y", "Z"]


class Plane(NamedTuple):
    axis: AXIS
    location: float

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Plane):
            return (
                bool(np.isclose(self.location, other.location))
                and self.axis == other.axis
            )
        return False


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
