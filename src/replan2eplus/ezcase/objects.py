from typing import NamedTuple
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ops.zones.create import create_zones
from geomeppy import IDF
from dataclasses import dataclass


@dataclass
class EzObjects:
    zones: list[Zone]
    surfaces: list[Surface]

    # airboundaries: list[Airboundary] = []
    # subsurfaces: list[Subsurface] = []
    # -> may call add materials / constructions several times..
    # self.materials: list[Material] = []
    # self.constructions: list[Construction] = []

    # self.airflownetwork = AirflowNetwork([], [], [])


def read_existing_objects(idf: IDF):
    zones, surfaces = create_zones(idf)
    return EzObjects(zones, surfaces)
