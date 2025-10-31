from replan2eplus.ops.afn.idfobject import IDFAFNSurface, IDFAFNZone
from replan2eplus.ops.afn.logic import determine_afn_objects
from replan2eplus.ops.airboundary.ezobject import Airboundary
from replan2eplus.ops.afn.interfaces import AFNWriter
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.zones.ezobject import Zone
from geomeppy import IDF
from replan2eplus.ops.afn.ezobject import AirflowNetwork
# from expression.collections import Seq


def select_afn_objects(
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
):
    afn_zones, afn_surfaces = determine_afn_objects(zones, airboundaries + subsurfaces)

    zone_names = [i.zone_name for i in afn_zones]
    sub_and_surface_names = [i.name for i in afn_surfaces]

    return AirflowNetwork(afn_zones, afn_surfaces), AFNWriter(
        zone_names, sub_and_surface_names
    )


def create_afn_objects(
    idf: IDF,
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
):
    if zones:
        if subsurfaces or airboundaries:
            airflow_network, afn_writer = select_afn_objects(
                zones, subsurfaces, airboundaries
            )
            if afn_writer.zone_names:  # TODO: potentially put this under test -> don't init the AFN if didnt find any AFN objects, also add a warning if the afn flag was true.. -> wont be able to access certain output variables
                afn_writer.write(idf)
            return airflow_network
    return AirflowNetwork([], [])
