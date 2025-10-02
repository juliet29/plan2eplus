from typing import Sequence
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.domain import Domain
from dataclasses import dataclass

from replan2eplus.geometry.plane import Plane
import shapely as sp

from replan2eplus.geometry.shapely_bounds import ShapelyBounds


@dataclass
class OrthoDomain:
    coords: list[Coord]
    plane: Plane | None = None

    @classmethod
    def from_tuple_list(cls, coords: Sequence[tuple[float | int, float | int]]):
        return cls([Coord(*i) for i in coords])

    @property
    def tuple_list(self):
        return [i.as_tuple for i in self.coords]

    @property
    def bounding_domain(self) -> Domain:
        poly = sp.Polygon(self.tuple_list)
        bounds = ShapelyBounds(*poly.bounds)
        return bounds.domain

    @property
    def centroid(self):
        return self.bounding_domain.centroid

        # create shapely polygon with coords
        # get its bounds..
