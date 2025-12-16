from dataclasses import dataclass, field
from typing import Literal, NamedTuple

from replan2eplus.visuals.styles.interfaces import (
    FontSize,
    Color,
    LineStyle,
    BoundingBox,
)
import math


@dataclass
class PlotStyles:
    @property
    def values(self):
        return self.__dict__


@dataclass
class AnnotationStyles(PlotStyles):
    # face_color: Color = "white"
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

    def update_bbox_color(self, color: Color):
        self.bbox["fc"] = color


@dataclass
class PolygonStyles(PlotStyles):
    fill: bool = False
    color: Color = "white"  # TODO check this..
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

    def afn_with_data(self, color: Color, linewidth: float):
        linewidth_map = max(3, math.ceil(linewidth))
        return LineStyles(color=color, linewidth=linewidth_map)
