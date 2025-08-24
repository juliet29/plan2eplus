from dataclasses import dataclass

from replan2eplus.ezobjects.surface import Surface
from replan2eplus.subsurfaces.interfaces import ZoneEdge


@dataclass
class Airboundary:
    surface: Surface
    edge: ZoneEdge


def get_unique_airboundaries(airboundaries: list[Airboundary]):
    return [i for i in airboundaries if i.edge.u in i.surface.zone_name]
