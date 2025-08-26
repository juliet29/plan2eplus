from typing import NamedTuple
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.domain import Plane
from replan2eplus.geometry.range import Range


from matplotlib.lines import Line2D


from dataclasses import dataclass

from replan2eplus.visuals.styles import Alignment

class MPlData(NamedTuple):
    xdata: list[float]
    ydata: list[float]


def split_coords(coords: list[Coord]):
    return MPlData([i.x for i in coords], [i.y for i in coords])


@dataclass
class Line:
    start: Coord
    end: Coord
    plane: Plane

    @property
    def alignment(self):
        # also depends on if exterior or interiro -> i exterior, always want outside.. but do we even really want labels or just legend? just for testing?
        if self.plane.axis == "X":
            return Alignment("right", "center", "vertical")._asdict()
        else:
            return Alignment("center", "top")._asdict()

    @property
    def to_line2D(self):
        return Line2D(
            *split_coords([self.start, self.end])
        )  # TODO think about cleaning this up..

    @property
    def centroid(self):
        return (
            Range(self.start.x, self.end.x).midpoint,
            Range(self.start.y, self.end.y).midpoint,
        )


