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


def get_afn_subsurfaces(afn_zones: list[Zone], subsurfaces: list[Subsurface]):
    potential_subsurface_names: list[str] = chain_flatten(
        [i.subsurface_names for i in afn_zones]
    )
    potential_subsurfaces = [
        i for i in subsurfaces if i.subsurface_name in potential_subsurface_names
    ]  # TODO filter function would help clean this up..
    afn_subsurfaces = get_unique_subsurfaces(potential_subsurfaces)
    return afn_subsurfaces


def get_afn_airboundaries(afn_zones: list[Zone], airboundaries: list[Airboundary]):
    afn_zone_names = [i.zone_name for i in afn_zones]
    possible_airboundaries = [
        i for i in airboundaries if i.surface.zone_name in afn_zone_names
    ]
    afn_airboundaries = get_unique_airboundaries(possible_airboundaries)
    return [i.surface for i in afn_airboundaries]


def select_afn_objects(
    zones: list[Zone], subsurfaces: list[Subsurface], airboundaries: list[Airboundary]
):
    afn_zones = [
        i for i in zones if len(i.potential_afn_surface_or_subsurface_names) >= 2
    ]
    anti_zones = [i for i in zones if i not in afn_zones]

    anti_surfaces_l1: list[Surface] = chain_flatten([i.surfaces for i in anti_zones])
    anti_surfaces_l2: list[str] = [i.neighbor for i in anti_surfaces_l1 if i.neighbor]
    anti_surfaces = [i.surface_name for i in anti_surfaces_l1] + anti_surfaces_l2

    anti_subsurfaces = chain_flatten([i.subsurface_names for i in anti_zones])

    afn_subsurfaces = [
        i
        for i in get_afn_subsurfaces(afn_zones, subsurfaces)
        if i.subsurface_name not in anti_subsurfaces
    ]

    afn_airboundaries = [
        i
        for i in get_afn_airboundaries(afn_zones, airboundaries)
        if i.surface_name not in anti_surfaces
    ]

    return AFNInputs(afn_zones, afn_subsurfaces, afn_airboundaries)


# TODO -> think this part of the code is untested..
def create_afn_objects(
    idf: IDF,
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
):
    inputs = select_afn_objects(zones, subsurfaces, airboundaries)
    idf.add_afn_simulation_control(inputs.sim_control)

    for zone in inputs.zones:
        idf.add_afn_zone(zone)
        idf.print_idf()

    for pair in zip(*inputs.surfaces_and_openings):
        afn_surface, afn_opening = pair
        idf.add_afn_surface(afn_surface)
        idf.add_afn_opening(afn_opening)
    idf.print_idf()

    return idf
