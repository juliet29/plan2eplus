from typing import Sequence
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.domain import Domain
from dataclasses import dataclass

from replan2eplus.geometry.planedef import Plane


@dataclass
class OrthoDomain:
    coords: list[Coord]
    plane: Plane | None = None

    # @property
    # def bounding_box(self) -> Domain:
    #     pass

    @classmethod
    def from_tuple_list(cls, coords: Sequence[tuple[float | int, float | int]]):
        return cls([Coord(*i) for i in coords])

    @property
    def tuple_coords(self):
        return [i.as_tuple for i in self.coords]
