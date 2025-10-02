from geomeppy.geom.polygons import Polygon3D
from replan2eplus.geometry.coords import Coord, Coordinate3D
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.ortho_domain import OrthoDomain
from replan2eplus.geometry.plane import AXIS, Plane
from replan2eplus.geometry.range import Range
from loguru import logger
from pathlib import Path
import sys
from rich import print

# TODO: move?
logger.add(sys.stdout, level="WARNING")


def get_location_of_fixed_plane(plane: AXIS, coords: list[Coordinate3D]):
    plane_locs = [coord.get_plane_axis_location(plane.lower()) for coord in coords]
    unique_loc = set(plane_locs)
    assert len(unique_loc) == 1
    return plane_locs[0]


def create_domain_from_coords_list(coords: list[Coord]):
    if len(coords) == 4:
        xs = sorted(set([i.x for i in coords]))
        ys = sorted(set([i.y for i in coords]))
        horz_range = Range(xs[0], xs[-1])
        vert_range = Range(ys[0], ys[-1])
        return Domain(horz_range, vert_range) # TODO can use shapely bounds.. 
    else:
        return OrthoDomain(coords)


def create_domain_from_coords(normal_axis: AXIS, coords: list[Coordinate3D]):
    def get_2D_coords(l1, l2):
        return [coord.get_pair(l1, l2) for coord in coords]

    match normal_axis:
        case "X":
            pair = ("y", "z")

        case "Y":
            pair = ("x", "z")

        case "Z":
            pair = ("x", "y")
        case _:
            raise Exception("Invalid Direction!")

    coords_2D = get_2D_coords(*pair)
    domain = create_domain_from_coords_list(coords_2D)

    location_of_fixed_plane = get_location_of_fixed_plane(normal_axis, coords)
    # TODO set plane function..
    # domain.plane = Plane(normal_axis, location_of_fixed_plane)
    plane = Plane(normal_axis, location_of_fixed_plane)

    if isinstance(domain, Domain):
        return Domain(
            domain.horz_range,
            domain.vert_range,
            plane,
        )
    else:
        return OrthoDomain(domain.coords, plane)


def compute_unit_normal(coords: list[tuple[float, float, float]]) -> AXIS:
    vector_map: dict[tuple[int, int, int], AXIS] = {
        (1, 0, 0): "X",
        (0, 1, 0): "Y",
        (0, 0, 1): "Z",
    }
    polygon = Polygon3D(coords)
    normal_vector = polygon.normal_vector
    nv = tuple([abs(int(i)) for i in normal_vector])
    assert len(nv) == 3

    # TODO this can be fixed by normalizing coords..
    try:
        return vector_map[nv]
    except:
        assert polygon.vertices
        flipped_vertices = reversed(polygon.vertices)

        logger.trace(
            f"These vertices are (counter)clockwise, but should be the other way around. Reorienting. \nOriginal: {polygon.vertices}. \nNew: {list(flipped_vertices)}"
        )  # TODO provide more context!
        normal_vector = polygon.normal_vector
        nv = tuple([abs(round(i)) for i in normal_vector])
        assert len(nv) == 3
        return vector_map[nv]
