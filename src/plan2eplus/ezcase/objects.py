from dataclasses import dataclass
from utils4plans.lists import chain_flatten

from geomeppyupdated import IDF

from plan2eplus.ops.afn.create import create_afn_objects
from plan2eplus.ops.afn.ezobject import AirflowNetwork
from plan2eplus.ops.airboundary.create import update_airboundary_constructions
from plan2eplus.ops.airboundary.ezobject import Airboundary
from plan2eplus.ops.schedules.user_interface import ScheduleInput
from plan2eplus.ops.subsurfaces.ezobject import Subsurface
from plan2eplus.ops.subsurfaces.create import create_subsurfaces
from plan2eplus.ops.surfaces.ezobject import Surface
from plan2eplus.ops.zones.create import create_zones
from plan2eplus.ops.zones.ezobject import Zone


@dataclass
class EzObjects:
    zones: list[Zone]
    surfaces: list[Surface]
    subsurfaces: list[Subsurface]
    airboundaries: list[Airboundary]
    airflow_network: AirflowNetwork

    @property
    def schedules(self):
        scheds: list[ScheduleInput] = []
        # TODO register all schedules here..
        if self.airflow_network.schedules:
            scheds.extend(self.airflow_network.schedules)
        return scheds

    # airboundaries: list[Airboundary] = []
    # subsurfaces: list[Subsurface] = []
    # -> may call add materials / constructions several times..
    # self.materials: list[Material] = []
    # self.constructions: list[Construction] = []

    # self.airflownetwork = AirflowNetwork([], [], [])


def read_existing_objects(idf: IDF, read_existing=True):
    if read_existing:
        zones, surfaces = create_zones(idf)
        subsurfaces = create_subsurfaces(
            None, surfaces, zones, idf
        )  # TODO correct arguments so that idf comes first
        airboundaries = update_airboundary_constructions(idf, [], zones, surfaces)
        afn = create_afn_objects(
            idf, zones, subsurfaces, airboundaries
        )  # TODO read existing in ..
        return EzObjects(zones, surfaces, subsurfaces, airboundaries, afn)
    return EzObjects([], [], [], [], AirflowNetwork([], []))
