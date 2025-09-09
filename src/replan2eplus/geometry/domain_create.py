from replan2eplus.geometry.nonant import Nonant, NonantEntries
from replan2eplus.geometry.range import Range
from replan2eplus.geometry.contact_points import (
    CardinalEntries,
    CornerEntries,
    CornerPoints,
)
from typing import Literal, NamedTuple, Union, NamedTuple
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.coords import Coord


# TODO the below is strictly subsurface related ---------- so should move to logic??


# TODO should this be a class method yay or nay? -> actuall
def create_domain_for_nonant(domain: Domain, loc: NonantEntries):
    coord = domain.nonant[loc]
    horz_dist = domain.nonant.horz_trirange.dist_between
    vert_dist = domain.nonant.vert_trirange.dist_between
    horz_range = Range(coord.x, coord.x + horz_dist)
    vert_range = Range(coord.y, coord.y + vert_dist)
    return Domain(horz_range, vert_range)

    # TODO return buffer of self..


# TODO: this goes to interfaces
class Dimension(NamedTuple):
    width: float
    height: float

    @property
    def as_tuple(self):
        return (self.width, self.height)


ContactEntries = Union[CornerEntries, CardinalEntries, Literal["CENTROID"]]


def create_domain_from_corner_point(
    coord: Coord, point_name: CornerEntries, dimensions: Dimension
):
    # dx = dimensions.width
    # dy = dimensions.height
    match point_name:
        case "NORTH_EAST":
            horz_range = Range(coord.x - dimensions.width, coord.x)
            vert_range = Range(coord.y - dimensions.height, coord.y)
        case "SOUTH_EAST":
            horz_range = Range(coord.x - dimensions.width, coord.x)
            vert_range = Range(coord.y, coord.y + dimensions.height)
        case "SOUTH_WEST":
            horz_range = Range(coord.x, coord.x + dimensions.width)
            vert_range = Range(coord.y, coord.y + dimensions.height)
        case "NORTH_WEST":
            horz_range = Range(coord.x, coord.x + dimensions.width)
            vert_range = Range(coord.y - dimensions.height, coord.y)
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
        # TODO case centroid
        case "CENTROID":
            return create_domain_from_centroid_and_dimensions(coord, dimensions)
        case _:
            raise Exception("Invalid point")


def place_domain(
    base_domain: Domain,
    nonant_loc: NonantEntries,
    nonant_contact_loc: CornerEntries,
    subsurface_contact_loc: CornerEntries,
    dimension: Dimension,
):
    nonant_domain = create_domain_for_nonant(base_domain, nonant_loc)
    nonant_coord = nonant_domain.corner[
        nonant_contact_loc
    ]  # TODO note this is a restriction and will need a match case here eventually..
    subsurf_domain = create_domain_from_contact_point_and_dimensions(
        nonant_coord, subsurface_contact_loc, dimension
    )
    return subsurf_domain
