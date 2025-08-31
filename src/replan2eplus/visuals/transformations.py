from typing import Protocol
from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.ezobjects import airboundary
from replan2eplus.ezobjects.afn import AirflowNetwork
from replan2eplus.ezobjects.airboundary import Airboundary
from replan2eplus.ezobjects.subsurface import Edge, NamedTuple, Subsurface
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.geometry.contact_points import CardinalPoints
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.directions import WallNormal, WallNormalNamesList
from replan2eplus.geometry.domain import Domain
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

from replan2eplus.visuals.interfaces import Line, split_coords
from replan2eplus.geometry.domain import compute_multidomain, expand_domain
from replan2eplus.ezobjects.epbunch_utils import set_difference


expansion_factor = 1.3


def domain_to_rectangle(domain: Domain):
    return Rectangle(
        (domain.horz_range.min, domain.vert_range.min),
        domain.horz_range.size,
        domain.vert_range.size,
        fill=False,
    )


# TODO write tests for this! and potentially move to geometry folder ..
def domain_to_line(domain: Domain):
    assert domain.plane
    plane = domain.plane
    if plane.axis == "Z":
        raise IDFMisunderstandingError("Can't flatten a domain in the Z Plane!")
    else:
        min_ = domain.horz_range.min
        max_ = domain.horz_range.max
    if plane.axis == "X":
        start = Coord(plane.location, min_)
        end = Coord(plane.location, max_)
    else:
        assert plane.axis == "Y"
        start = Coord(min_, plane.location)
        end = Coord(max_, plane.location)
    return Line(start, end, plane)


# this is a pretty generic fx -> utils4plans -> filter, get1 throw error
def get_zones(name, zones: list[Zone]):
    # NOTE: changing this for studies!
    possible_zones = [i for i in zones if name in i.zone_name]
    assert len(possible_zones) == 1, f"Name: {name}, poss_zones: {possible_zones}"
    return possible_zones[0]


# TODO: think about sharing with the base plot..
def calculate_cardinal_domain(
    zones: list[Zone], cardinal_expansion_factor=expansion_factor
):
    total_domain = compute_multidomain([i.domain for i in zones])

    cardinal_domain = expand_domain(total_domain, cardinal_expansion_factor)

    return cardinal_domain


def subsurface_to_connection_line(
    domain: Domain,
    edge: Edge,
    zones: list[Zone],
    cardinal_coords: CardinalPoints,
):
    space_a, space_b = edge

    middle_coord = Coord(*domain_to_line(domain).centroid)

    zone_a = get_zones(space_a, zones)
    coord_a = zone_a.domain.centroid
    if space_b in WallNormalNamesList:
        coord_b = cardinal_coords.dict_[space_b]
    else:
        zone_b = get_zones(space_b, zones)
        coord_b = zone_b.domain.centroid

    points = [coord_a, middle_coord, coord_b]
    return Line2D(*split_coords(points))


# TODO this is kind of its own thing!
class SurfaceOrg(NamedTuple):
    non_afn_surfaces: list[Surface | Subsurface]
    windows: list[Subsurface]
    doors: list[Subsurface]
    airboundaries: list[Airboundary]


def organize_subsurfaces_and_surfaces(
    afn: AirflowNetwork, airboundaries: list[Airboundary], subsurfaces: list[Subsurface]
):
    non_afn_surfaces = [i.surface for i in afn.non_afn_airboundaries(airboundaries)]
    not_in_afn = non_afn_surfaces + afn.non_afn_subsurfaces(subsurfaces)
    windows = filter(lambda x: x.is_window, afn.subsurfaces)
    doors = filter(lambda x: x.is_door, afn.subsurfaces)

    return SurfaceOrg(
        not_in_afn,
        list(windows),
        list(doors),
        afn.airboundaries,
    )


# TODO this is an experiment -> will keep w/ list comprehensions for now..


# TODO do a similar thing for AFN -> let this be the basis of how structure the ezobject -> ie need it to have an edge
# required properties ~ protocol -> edge, domain -> basically a superset of surface + subsurface


class ConnectionOrg(NamedTuple):
    baseline: list[Airboundary | Subsurface]
    afn: list[Subsurface | Airboundary]


def organize_connections(
    afn: AirflowNetwork, airboundaries: list[Airboundary], subsurfaces: list[Subsurface]
):
    # non_afn = afn.non_afn_airboundaries(airboundaries) + afn.non_afn_subsurfaces(
    #     subsurfaces
    # )
    return ConnectionOrg(airboundaries + subsurfaces, afn.surfacelike_objects)
