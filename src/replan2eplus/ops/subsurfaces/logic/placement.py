from replan2eplus.geometry.nonant import Nonant, NonantEntries
from replan2eplus.geometry.range import Range
from replan2eplus.geometry.contact_points import (
    CardinalEntries,
    CornerEntries,
    CornerPoints,
)
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.coords import Coord
from replan2eplus.ops.subsurfaces.interfaces import Dimension
from replan2eplus.ops.subsurfaces.interfaces import ContactEntries


# TODO should this be a class method yay or nay? -> actuall
def create_domain_for_nonant(domain: Domain, loc: NonantEntries):
    coord = domain.nonant[loc]
    horz_dist = domain.nonant.horz_trirange.dist_between
    vert_dist = domain.nonant.vert_trirange.dist_between
    horz_range = Range(coord.x, coord.x + horz_dist)
    vert_range = Range(coord.y, coord.y + vert_dist)
    return Domain(horz_range, vert_range)


def create_domain_from_corner_point(
    coord: Coord, point_name: CornerEntries, dimensions: Dimension
):
    dx = dimensions.width
    dy = dimensions.height
    match point_name:
        case "NORTH_EAST":
            horz_range = Range(coord.x - dx, coord.x)
            vert_range = Range(coord.y - dimensions.height, coord.y)
        case "SOUTH_EAST":
            horz_range = Range(coord.x - dx, coord.x)
            vert_range = Range(coord.y, coord.y + dy)
        case "SOUTH_WEST":
            horz_range = Range(coord.x, coord.x + dx)
            vert_range = Range(coord.y, coord.y + dy)
        case "NORTH_WEST":
            horz_range = Range(coord.x, coord.x + dx)
            vert_range = Range(coord.y - dy, coord.y)
        case _:
            raise Exception("Invalid corner point!")

    return Domain(horz_range, vert_range)


def create_domain_from_cardinal_loc(
    coord: Coord, point_name: CardinalEntries, dimensions: Dimension
):
    dx = dimensions.width
    dy = dimensions.height
    half_dx = dx / 2
    half_dy = dy / 2
    match point_name:
        case "NORTH":
            horz_range = Range(coord.x - half_dx, coord.x + half_dx)
            vert_range = Range(coord.y - dy, coord.y)
        case "SOUTH":
            horz_range = Range(coord.x - half_dx, coord.x + half_dx)
            vert_range = Range(coord.y, coord.y + dy)
        case "EAST":
            horz_range = Range(coord.x - dx, coord.x)
            vert_range = Range(coord.y - half_dy, coord.y + half_dy)
        case "WEST":
            horz_range = Range(coord.x, coord.x + dx)
            vert_range = Range(coord.y - half_dy, coord.y + half_dy)
        case _:
            raise Exception("Invalid corner point!")

    return Domain(horz_range, vert_range)


def create_domain_from_centroid_and_dimensions(coord: Coord, dimensions: Dimension):
    dx = dimensions.width
    dy = dimensions.height
    half_dx = dx / 2
    half_dy = dy / 2
    horz_range = Range(coord.x - half_dx, coord.x + half_dx)
    vert_range = Range(coord.y - half_dy, coord.y + half_dy)
    return Domain(horz_range, vert_range)


def create_domain_from_contact_point_and_dimensions(
    coord: Coord, point_name: ContactEntries, dimensions: Dimension
):  # TODO rename to contact_loc and make it explicit that coord => nonant coord..+ add to conventions.md
    """
    coord => nonant loc
    point_name => for the subsurface..
    """
    match point_name:
        case "NORTH_EAST" | "SOUTH_EAST" | "SOUTH_WEST" | "NORTH_WEST":
            return create_domain_from_corner_point(coord, point_name, dimensions)
        case "NORTH" | "SOUTH" | "EAST" | "WEST":
            return create_domain_from_cardinal_loc(coord, point_name, dimensions)
        case "CENTROID":
            return create_domain_from_centroid_and_dimensions(coord, dimensions)
        case _:
            raise Exception("Invalid point")


def get_nonant_coord(domain: Domain, point_name: ContactEntries):
    match point_name:
        case "NORTH_EAST" | "SOUTH_EAST" | "SOUTH_WEST" | "NORTH_WEST":
            return domain.corner[point_name]
        case "NORTH" | "SOUTH" | "EAST" | "WEST":
            return domain.cardinal[point_name]
        case "CENTROID":
            return domain.centroid
        case _:
            raise Exception("Invalid point")


def place_domain(
    base_domain: Domain,
    nonant_loc: NonantEntries,
    nonant_contact_loc: ContactEntries,
    subsurface_contact_loc: ContactEntries,
    dimension: Dimension,
):
    nonant_domain = create_domain_for_nonant(base_domain, nonant_loc)
    nonant_coord = get_nonant_coord(nonant_domain, nonant_contact_loc)
    subsurf_domain = create_domain_from_contact_point_and_dimensions(
        nonant_coord, subsurface_contact_loc, dimension
    )
    return subsurf_domain
