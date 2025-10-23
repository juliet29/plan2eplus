from dataclasses import dataclass

from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.subsurfaces.ezobject import Edge


@dataclass
class Airboundary:
    surface: Surface
    edge: Edge

    @property
    def domain(self):
        return self.surface.domain

    @property
    def display_name(self):
        return self.surface.display_name


def get_unique_airboundaries(airboundaries: list[Airboundary]):
    return [i for i in airboundaries if i.edge.space_a in i.surface.zone_name]
