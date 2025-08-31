from dataclasses import dataclass
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from typing import NamedTuple, Literal
from replan2eplus.ezobjects.subsurface import Edge
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.geometry.contact_points import CardinalPoints
from replan2eplus.geometry.domain import Domain
from replan2eplus.visuals.transformations import (
    domain_to_rectangle,
    domain_to_line,
    subsurface_to_connection_line,
)
from matplotlib.axes import Axes

# TODO move to styles...
Color = Literal["navy", "deepskyblue", "gray", "snow", "saddlebrown", "white", "black"]
LineStyle = Literal[
    "-",
    "--",
    "-.",
    ":",
]


@dataclass
class PlotStyles:
    @property
    def values(self):
        return self.__dict__


@dataclass
class RectangleStyles(PlotStyles):
    fill: bool = False
    facecolor: Color = "white"  # TODO check this..
    edgecolor: Color = "black"
    alpha: float = 1
    linewidth: int = 4
    zorder: int = 0


@dataclass
class LineStyles(PlotStyles):
    color: Color
    linestyle: LineStyle = "-"
    gapcolor: Color = "white"
    alpha: float = 1
    linewidth: int = 4
    zorder: int = 1


# is this actually a typed dict?
class SurfaceStyles(NamedTuple):
    non_afn_surfaces = LineStyles(color="gray", zorder=2)
    windows = LineStyles(color="deepskyblue", zorder=2)
    doors = LineStyles(color="saddlebrown", zorder=2)
    airboundaries = LineStyles(
        color="deepskyblue", linestyle=":", gapcolor="white", zorder=2
    )


class ConnectionStyles(NamedTuple):
    baseline = LineStyles(color="gray", linewidth=6, alpha=0.4)
    afn = LineStyles(color="navy", linewidth=3)
    # airboundaries = LineStyles(color="deepskyblue", linestyle=":", gapcolor="white")
    # non_afn_surfaces = LineStyles(color="gray")


def add_rectangles(domains: list[Domain], style: RectangleStyles, axes: Axes):
    for domain in domains:
        rectangle = domain_to_rectangle(domain)
        rectangle.set(**style.values)
        axes.add_artist(rectangle)
    return axes


def add_surface_lines(domains: list[Domain], style: LineStyles, axes: Axes):
    for domain in domains:
        line = domain_to_line(domain).to_line2D
        line.set(**style.values)
        axes.add_artist(line)
    return axes


def add_connection_lines(
    domains: list[Domain],
    edges: list[Edge],
    zones: list[Zone],
    cardinal_coords: CardinalPoints,
    style: LineStyles,
    axes: Axes,
):
    for domain, edge in zip(domains, edges):
        line = subsurface_to_connection_line(domain, edge, zones, cardinal_coords)
        line.set(**style.values)
        axes.add_artist(line)
    return axes
