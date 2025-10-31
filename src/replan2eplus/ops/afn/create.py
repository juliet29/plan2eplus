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

    return AirflowNetwork(afn_zones, afn_surfaces)


def create_afn_objects(
    idf: IDF,
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
):
    if zones:
        if subsurfaces or airboundaries:
            afn = select_afn_objects(zones, subsurfaces, airboundaries)
            zone_names = [i.zone_name for i in afn.zones]
            sub_and_surface_names = [i.name for i in afn.afn_surfaces]
            if afn.zones:
                # TODO: potentially put this under test -> don't init the AFN if didnt find any AFN objects, also add a warning if the afn flag was true.. -> wont be able to access certain output variables
                AFNWriter(zone_names, sub_and_surface_names).write(idf)

            return afn
    return AirflowNetwork([], [])
