from replan2eplus.afn.interfaces import AFNInputs
from replan2eplus.ezobjects.airboundary import Airboundary, get_unique_airboundaries
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.idfobjects.afn import (
    AFNKeys,
)
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.subsurfaces.presentation import chain_flatten
from replan2eplus.subsurfaces.utils import get_unique_subsurfaces
from replan2eplus.afn.interfaces import AFNInputs


def select_afn_objects(zones: list[Zone], subsurfaces: list[Subsurface], airboundaries: list[Airboundary] ):
    afn_zones = [
        i for i in zones if len(i.potential_afn_surface_or_subsurface_names) >= 2
    ]

    # get afn subsurface objects..
    potential_subsurface_names: list[str] = chain_flatten(
        [i.subsurface_names for i in afn_zones]
    )
    potential_subsurfaces = [
        i for i in subsurfaces if i.subsurface_name in potential_subsurface_names
    ]
    afn_subsurfaces = get_unique_subsurfaces(potential_subsurfaces)

    # get afn surface objects
    # potential_surfaces: list[Surface] = chain_flatten(
    #     [i.afn_surfaces for i in afn_zones]
    # )
    # filter to removed duplicates.. for now do dummy!, then think more about this upon entry... -> do afn surfaces need to carry an edge with them?

    # TODO get airboundaries! -> need to do materials first!
    afn_zone_names = [i.zone_name for i in afn_zones]
    possible_airboundaries = [i for i in airboundaries if i.surface.zone_name in afn_zone_names]
    afn_airboundaries = get_unique_airboundaries(possible_airboundaries)
    # [i for i in airboundaries if i.edge.u in i.surface.zon]
    afn_airboundary_surfaces = [i.surface for i in afn_airboundaries]

    return AFNInputs(afn_zones, afn_subsurfaces, afn_airboundary_surfaces) 


def create_afn_objects(inputs: AFNInputs, idf: IDF):
    idf.add_afn_simulation_control(inputs.sim_control)

    for zone in inputs.zones:
        idf.add_afn_zone(zone)

    for pair in zip(*inputs.surfaces_and_openings):
        afn_surface, afn_opening = pair
        idf.add_afn_surface(afn_surface)
        idf.add_afn_opening(afn_opening)

    return idf
