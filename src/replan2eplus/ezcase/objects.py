from dataclasses import dataclass

from geomeppy import IDF

from replan2eplus.ops.afn.ezobject import AirflowNetwork
from replan2eplus.ops.airboundary.create import update_airboundary_constructions
from replan2eplus.ops.airboundary.ezobject import Airboundary
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.subsurfaces.create import create_subsurfaces
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.zones.create import create_zones
from replan2eplus.ops.zones.ezobject import Zone


@dataclass
class EzObjects:
    zones: list[Zone]
    surfaces: list[Surface]
    subsurfaces: list[Subsurface]
    airboundaries: list[Airboundary]
    airflow_network: AirflowNetwork

    # airboundaries: list[Airboundary] = []
    # subsurfaces: list[Subsurface] = []
    # -> may call add materials / constructions several times..
    # self.materials: list[Material] = []
    # self.constructions: list[Construction] = []

    # self.airflownetwork = AirflowNetwork([], [], [])


def read_existing_objects(idf: IDF):
    zones, surfaces = create_zones(idf)
    subsurfaces = create_subsurfaces(
        None, surfaces, zones, idf
    )  # TODO correct arguments so that idf comes first
    airboundaries = update_airboundary_constructions(idf, [], zones, surfaces)
    afn = AirflowNetwork([], [])  # TODO read existing in ..
    return EzObjects(zones, surfaces, subsurfaces, airboundaries, afn)
