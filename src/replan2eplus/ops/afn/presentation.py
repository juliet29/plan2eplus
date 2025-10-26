from expression.collections import Seq
from replan2eplus.ops.afn.interfaces import AFNInputs
from replan2eplus.ops.afn.logic import determine_afn_objects
from replan2eplus.ops.airboundary.ezobject import Airboundary, get_unique_airboundaries
from replan2eplus.ops.afn.writer import AFNWriter
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.zones.ezobject import Zone
from replan2eplus.idfobjects.afn import (
    AFNKeys,
)
from geomeppy import IDF
from utils4plans.lists import chain_flatten
from replan2eplus.ops.subsurfaces.utils import get_unique_subsurfaces
from replan2eplus.ezobjects.afn import AirflowNetwork


def select_afn_objects(
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
    # surfaces: list[Surface],
):
    afn_zones, afn_surfaces = determine_afn_objects(zones, airboundaries + subsurfaces)

    zone_names = [i.zone_name for i in afn_zones]
    sub_and_surface_names = [i.name for i in afn_surfaces]
    afn_airboundaries = 

    return AirflowNetwork(afn_zones, afn_subsurfaces, afn_airboundaries), AFNWriter(
        zone_names, sub_and_surface_names
    )


# TODO -> this should be the only thing in presentation
def create_afn_objects(
    idf: IDF,
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
):
    afn_holder, afn_writer = select_afn_objects(zones, subsurfaces, airboundaries)
    afn_writer.write(idf)
    return afn_holder
