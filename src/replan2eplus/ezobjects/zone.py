from eppy.bunch_subclass import EpBunch
from dataclasses import dataclass, field
from replan2eplus.errors import BadlyFormatedIDFError
from replan2eplus.ezobjects.base import EZObject

import replan2eplus.epnames.keys as epkeys
from utils4plans.lists import sort_and_group_objects_dict
from replan2eplus.ezobjects.surface import Surface
from typing import TypeVar

from replan2eplus.geometry.directions import WallNormal
from utils4plans.lists import chain_flatten
from replan2eplus.ezobjects.name import decompose_idf_name

T = TypeVar("T")


@dataclass
class DirectedSurfaces:
    NORTH: list[Surface]
    EAST: list[Surface]
    SOUTH: list[Surface]
    WEST: list[Surface]
    UP: list[Surface]
    DOWN: list[Surface]


@dataclass
class Zone:
    # _epbunch: EpBunch
    # room_name: str
    zone_name: str

    # expected_key: str = epkeys.ZONE
    surfaces: list[Surface] = field(default_factory=list)

    def __rich_repr__(self):
        yield "room_name", self.room_name
        yield "idf_name", self.zone_name
        yield "domain", self.domain
        yield "num_surfaces", len(self.surfaces)
        yield "num_subsurfaces", len(self.subsurface_names)
        yield "surface_display_names", self.surface_display_names
        yield "subsurface_names", self.subsurface_names

    @property
    def room_name(self):
        idf_name = decompose_idf_name(self.zone_name)
        return idf_name.plan_name

    # @property
    # def zone_name(self):  # idf name?
    #     return self._idf_name

    @property
    def surface_names(self):
        return [i.surface_name for i in self.surfaces]

    @property
    def surface_display_names(self):
        return sorted([i.display_name for i in self.surfaces])

    @property
    def subsurface_names(self) -> list[str]:
        return chain_flatten(
            [i.subsurface_names for i in self.surfaces if i.subsurface_names]
        )

    @property
    def afn_surfaces(self):
        return [i for i in self.surfaces if i.is_airboundary]

    @property
    def potential_afn_surface_or_subsurface_names(self):
        surface_names = [i.surface_name for i in self.afn_surfaces]
        return surface_names + self.subsurface_names

    @property
    def directed_surfaces(self):
        d: dict[WallNormal, list[Surface]] = sort_and_group_objects_dict(
            self.surfaces, lambda x: x.direction
        )
        d_names = {k.name: v for k, v in d.items()}
        return d_names  # DirectedSurfaces(**d_names)

    @property
    def domain(self):
        floors = self.directed_surfaces[WallNormal.DOWN.name]
        assert len(floors) == 1, BadlyFormatedIDFError(
            f"Zone {self.zone_name} has 0 or more than 2 floors!: {floors}"
        )
        return floors[0].domain  # TODO check the plane..


# TODO: get zones by zone_name
def get_zones(name, zones: list[Zone]):
    # NOTE: changing this for studies!
    possible_zones = [i for i in zones if name == i.room_name]
    assert len(possible_zones) == 1, (
        f"Name: {name}, poss_zones: {possible_zones}. Zones to choose from: {[i.room_name for i in zones]}"
    )
    return possible_zones[0]
