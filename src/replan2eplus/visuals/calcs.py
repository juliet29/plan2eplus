from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.domain import Domain
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from dataclasses import dataclass

from replan2eplus.geometry.range import Range


def domain_to_mpl_patch(domain: Domain):
    return Rectangle(
        (domain.horz_range.min, domain.vert_range.min),
        domain.horz_range.size,
        domain.vert_range.size,
        fill=False,
    )


@dataclass
class Line:
    start: Coord
    end: Coord

    @property
    def pair(self):
        return [self.start, self.end]

    @property
    def to_line2D(self):
        return Line2D(xdata=[i.x for i in self.pair], ydata=[i.y for i in self.pair]) #TODO think about cleaning this up.. 

    @property
    def centroid(self):
        return (
            Range(self.start.x, self.end.x).midpoint,
            Range(self.start.y, self.end.y).midpoint,
        )


def domain_to_line(domain: Domain):
    assert domain.plane
    plane = domain.plane
    if plane.axis == "Z":
        raise IDFMisunderstandingError("Can't flatten a domain in the Z Plane!")
    else:
        min_ = domain.horz_range.min
        max_ = domain.horz_range.max
    if plane.axis == "X":
        start = Coord(plane.location, min_)
        end = Coord(plane.location, max_)
    else:
        assert plane.axis == "Y"
        start = Coord(min_, plane.location)
        end = Coord(max_, plane.location)
    return Line(start, end)
