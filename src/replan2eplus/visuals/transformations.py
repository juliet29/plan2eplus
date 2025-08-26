from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.geometry.contact_points import CardinalPoints
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.directions import WallNormal, WallNormalNamesList
from replan2eplus.geometry.domain import Domain
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

from replan2eplus.visuals.interfaces import Line, split_coords


def domain_to_rectangle(domain: Domain):
    return Rectangle(
        (domain.horz_range.min, domain.vert_range.min),
        domain.horz_range.size,
        domain.vert_range.size,
        fill=False,
    )


# TODO write tests for this!
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


def subsurface_to_connection_line(
    subsurface: Subsurface, zones: list[Zone], cardinal_coords: CardinalPoints
):
    space_a, space_b = subsurface.edge
    middle_coord = Coord(*domain_to_line(subsurface.domain).centroid)
    zone_a = get_zones(space_a, zones)
    coord_a = zone_a.domain.centroid
    if space_b in WallNormal:
        assert isinstance(space_b, WallNormal)
        coord_b = cardinal_coords.dict_[space_b.name]
    else:
        zone_b = get_zones(space_b, zones)
        coord_b = zone_b.domain.centroid

    points = [coord_a, middle_coord, coord_b]
    return Line2D(*split_coords(points))
# TODO do a similar thing for AFN -> let this be the basis of how structure the ezobject -> ie need it to have an edge
# required properties ~ protocol -> edge, domain -> basically a superset of surface + subsurface