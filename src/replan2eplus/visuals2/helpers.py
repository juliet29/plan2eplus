from dataclasses import dataclass, field
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from typing import NamedTuple, Literal, TypedDict
from replan2eplus.ezobjects.subsurface import Edge
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.geometry.contact_points import CardinalPoints
from replan2eplus.geometry.coords import Coord
from replan2eplus.geometry.domain import Domain
from replan2eplus.visuals.transformations import (
    domain_to_rectangle,
    domain_to_line,
    subsurface_to_connection_line,
)
from matplotlib.axes import Axes

FontSize = Literal[
    "xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"
]

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


# separate probably..


# @dataclass(frozen=True)
class BoundingBox(TypedDict):
    boxstyle: str
    ec: Color
    fc: Color
    alpha: int


@dataclass
class AnnotationStyles(PlotStyles):
    bbox: BoundingBox = field(
        default_factory=lambda: {
            "boxstyle": "round,pad=0.2",
            "ec": "black",
            "fc": "white",
            "alpha": 1,
        }
    )
    fontsize: FontSize = "medium"
    horizontalalignment: Literal["left", "center", "right"] = "center"
    verticalalignment: Literal["top", "center", "baseline", "bottom"] = "center"
    rotation: Literal["vertical"] | None = None
    zorder = 10


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
    label: str = ""

    def reset_label(self):
        self.label = ""


# is this actually a typed dict?
class SurfaceStyles(NamedTuple):
    non_afn_surfaces = LineStyles(color="gray", zorder=2, label="Not in AFN")
    windows = LineStyles(color="deepskyblue", zorder=2, label="Window")
    doors = LineStyles(color="saddlebrown", zorder=2, label="Door")
    airboundaries = LineStyles(
        color="deepskyblue",
        linestyle=":",
        gapcolor="white",
        zorder=2,
        label="Airboundary",
    )


class ConnectionStyles(NamedTuple):
    baseline = LineStyles(color="gray", linewidth=12, alpha=0.1)
    afn = LineStyles(color="navy", linewidth=3)


def add_rectangles(domains: list[Domain], style: RectangleStyles, axes: Axes):
    for domain in domains:
        rectangle = domain_to_rectangle(domain)
        rectangle.set(**style.values)
        axes.add_artist(rectangle)
    return axes


def add_surface_lines(domains: list[Domain], style: LineStyles, axes: Axes):
    for ix, domain in enumerate(domains):
        if ix != 0:
            style.label = ""
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


class AnnotationPair(NamedTuple):
    coord: Coord
    name: str


def add_annotations(
    annotation_pair: list[AnnotationPair],
    style: AnnotationStyles,
    axes: Axes,
):
    for coord, name in annotation_pair:
        axes.text(*coord.as_tuple, s=name, **style.values)
    return axes
