from matplotlib.lines import Line2D
from replan2eplus.geometry.coords import Coord
import shapely
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.axes import Axes
import numpy as np

from replan2eplus.visuals.styles.artists import Color


def line_to_coords(line: Line2D, value_sign: int):
    data = list(line.get_data())
    coord_a, coord_b, coord_c = zip(*data)
    if value_sign < 0:
        return Coord(*coord_a), Coord(*coord_b)
    else:
        return Coord(*coord_b), Coord(*coord_c)


def create_triangle_patch(
    line_: Line2D,
    value_sign: int = 1,
    EXPANSION_FACTOR=1.1,
):
    assert EXPANSION_FACTOR > 1
    coords = line_to_coords(line_, value_sign)
    line = shapely.LineString([i.as_tuple for i in coords])

    dist_along = (line.length / 2) * EXPANSION_FACTOR
    # dist_along = 0.5 * EXPANSION_FACTOR
    if value_sign < 0:
        dist_along *= -1
    p0 = line.interpolate(dist_along)

    actual_dist_along = 0.1  # line.centroid.distance(p0)
    # print(f"{actual_dist_along=}")

    p1 = line.parallel_offset(
        actual_dist_along, "right"
    ).centroid  # TODO use nearest point instead..
    p2 = line.parallel_offset(actual_dist_along, "left").centroid
    shapely.Polygon([p0, p1, p2]).is_valid
    # coords = triangle.exterior.coords
    return Polygon(shapely.get_coordinates([p0, p1, p2]))


def add_arrows(
    lines: list[Line2D],
    value_signs: list[int],
    values: list[float] | np.ndarray,
    axes: Axes,
    colors: list[Color] = ["black"],
):
    assert len(lines) == len(value_signs)
    patches = [
        create_triangle_patch(line, sign, 1 + 10e-2 + value)
        for line, sign, value in zip(lines, value_signs, values)
    ]
    axes.add_collection(PatchCollection(patches, facecolor=colors, edgecolor="black"))
    return axes
