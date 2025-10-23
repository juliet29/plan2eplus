from replan2eplus.geometry.directions import WallNormal
from replan2eplus.geometry.contact_points import CardinalEntries, CornerEntries
from replan2eplus.geometry.nonant import NonantEntries
from typing import Callable, Literal, NamedTuple, Union


class ZoneDirectionEdge(NamedTuple):
    """for convenience, spaces are described using room names, not the idf names"""

    space_a: str
    space_b: WallNormal


class ZoneEdge(NamedTuple):
    """for convenience, spaces are described using room names, not the idf names"""

    space_a: str
    space_b: str


class Dimension(NamedTuple):
    width: float
    height: float

    @property
    def as_tuple(self):
        return (self.width, self.height)

    @property
    def area(self):
        return self.width * self.height

    def modify(self, fx: Callable[[float], float]):
        return self.__class__(fx(self.width), fx(self.height))

    def modify_area(self, factor: float):
        # preserves aspect ratio
        sqrt_val = factor ** (1 / 2)
        return self.__class__.modify(self, lambda x: sqrt_val * x)


ContactEntries = Union[CornerEntries, CardinalEntries, Literal["CENTROID"]]


class Location(NamedTuple):
    nonant_loc: NonantEntries
    nonant_contact_loc: ContactEntries
    subsurface_contact_loc: ContactEntries


# TODO make some defaults!


SubsurfaceType = Literal["Door", "Window"]
SubsurfaceKey = Literal[
    "DOOR", "WINDOW", "DOOR:INTERZONE", "FENESTRATIONSURFACE:DETAILED"
]
