from replan2eplus.geometry.directions import WallNormal, WallNormalNamesList
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


# subsurface_options = [
#     "DOOR",
#     "WINDOW",
#     "DOOR:INTERZONE",
# ]  # TODO arg thing since now have literal..

# display_map = {"DOOR": "Door", "WINDOW": "Window", "DOOR:INTERZONE": "Door"}


class Edge(NamedTuple):
    space_a: str
    space_b: str

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Edge):
            return frozenset(self.as_tuple) == frozenset(other.as_tuple)
        raise Exception(f"{other} does not have type Edge")

    def __hash__(self) -> int:
        fe = frozenset(self.as_tuple)
        return hash(fe)

    @property
    def is_directed_edge(self):
        return (
            self.space_a in WallNormalNamesList or self.space_b in WallNormalNamesList
        )

    @property
    def as_tuple(self):
        return (self.space_a, self.space_b)

    @property
    def sorted_directed_edge(self):
        if self.is_directed_edge:
            zone, drn = sorted(
                [self.space_a, self.space_b], key=lambda x: x in WallNormalNamesList
            )  # NOTE: order is (false=0, true=1)
            return (zone, WallNormal[drn])
        else:
            raise Exception("This is not a directed edge!")
