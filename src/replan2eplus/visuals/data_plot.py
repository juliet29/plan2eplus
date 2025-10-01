from dataclasses import dataclass
from typing import Callable, Literal

import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from xarray import DataArray

from replan2eplus.ezobjects.afn import Airboundary, set_difference, set_intersection
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.geometry.contact_points import calculate_cardinal_points
from replan2eplus.visuals.axis_modifications import (
    add_connection_lines,
    add_rectangles,
)
from replan2eplus.visuals.base_plot import BasePlot
from replan2eplus.visuals.styles.artists import (
    ConnectionStyles,
    RectangleStyles,
)
from replan2eplus.visuals.transform import (
    EXPANSION_FACTOR,
)
from replan2eplus.visuals.arrow import add_arrows
import math
from matplotlib.colorbar import Colorbar
from matplotlib.colors import Colormap, Normalize, TwoSlopeNorm


ColorBarFx = Callable[
    [list[float] | np.ndarray, Axes],
    tuple[tuple[Colorbar], Colormap, Normalize | TwoSlopeNorm],
]


def pressure_colorbar(data: list[float] | np.ndarray, ax: Axes):
    expansion = 1.3
    if len(data) == 1:
        res = data[0]
        norm = colors.Normalize(vmin=res - expansion, vmax=res + expansion)
        cmap = mpl.colormaps["YlOrRd_r"]

    else:
        min_, max_ = (
            min(data) * expansion,
            max(data) * expansion,
        )  # TODO come up with a netter way of doing this expansion thing / figuring out the limits of data to show..
        # TODO reverse colors for pressure!

        if max_ <= 0:
            norm = colors.Normalize(vmin=min_, vmax=max_)
            cmap = mpl.colormaps["YlOrRd_r"]
        else:
            center = 0

            norm = colors.TwoSlopeNorm(vmin=min_, vcenter=center, vmax=max_)

            cmap = mpl.colormaps["RdYlBu"]

    bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap),
            orientation="vertical",
            label="Total Pressure [Pa]",
            ax=ax,
            # shrink=0.5
            # TODO pass in the label
        ),
    )
    return bar, cmap, norm


def temperature_colorbar(data: list[float] | np.ndarray, ax: Axes):
    cmap = mpl.colormaps["YlOrRd"]
    min_, max_ = min(data), max(data)
    norm = colors.Normalize(vmin=min_, vmax=max_)
    bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap),
            orientation="vertical",
            label="Temperature [ºC]",
            ax=ax,
        ),
    )
    return bar, cmap, norm


def flow_colorbar(data: list[float] | np.ndarray, ax: Axes):
    cmap = mpl.colormaps["PuBu"]
    min_, max_ = min(data), max(data)
    norm = colors.Normalize(vmin=min_, vmax=max_)
    bar = (
        plt.colorbar(
            cm.ScalarMappable(norm=norm, cmap=cmap),
            orientation="vertical",
            label="Volume Flow Rate [m3/s]",
            ax=ax,
        ),
    )
    return bar, cmap, norm


def filter_data_arr(data_arr: DataArray, geom_names: list[str]):
    space_names_to_compare = data_arr.space_names.values  # TODO replace..
    diff = set_difference(space_names_to_compare, geom_names)
    if diff:
        intersect = set_intersection(space_names_to_compare, geom_names)

        assert intersect, (
            f"Some space_names are not contained in the expected geometry, and there is no intersection! -> {diff}. "
        )
        res = data_arr.sel(space_names=intersect)
        return res
    return data_arr


@dataclass
class DataPlot(BasePlot):
    zones: list[Zone]
    cardinal_expansion_factor: float = EXPANSION_FACTOR
    extents_expansion_factor: float = EXPANSION_FACTOR

    def __post_init__(self):
        super().__post_init__()
        self.zone_dict = {i.zone_name.upper(): i for i in self.zones}
        self.zone_names = [i.zone_name.upper() for i in self.zones]

    def plot_zones_with_data(
        self, data_arr_: DataArray, colorbar_fx: ColorBarFx = pressure_colorbar
    ):
        data_arr = filter_data_arr(data_arr_, self.zone_names)
        bar, cmap, norm = colorbar_fx(data_arr.values, self.axes)
        styles = [
            RectangleStyles(fill=True, color=cmap(norm(i))) for i in data_arr.values
        ]
        domains = [self.zone_dict[i].domain for i in data_arr.space_names.values]

        add_rectangles(domains, styles, self.axes)
        # grey for zones not included..
        non_included_zones = set_difference(
            self.zone_names, data_arr.space_names.values
        )
        add_rectangles(
            [self.zone_dict[i].domain for i in non_included_zones],
            [RectangleStyles(fill=True, color="gray")],
            self.axes,
        )

        return self

    def plot_connections_with_data(
        self,
        data_arr_: DataArray,
        subsurfaces: list[Subsurface],
        airboundaries: list[Airboundary],
        WIDTH_FACTOR=10,
        ARROW_FACTOR=12,
    ):
        # TODO check dimensions of the dataarray..
        # TODO this should be handled elsewhere -> in post init? if have zones have everything else, so this should be passed.. unique surfaces should be calculated immediately in the base_plot..
        self.subsurface_dict = {i.subsurface_name.upper(): i for i in subsurfaces}
        self.airboundary_dict = {
            i.surface.surface_name.upper(): i for i in airboundaries
        }
        self.subsurface_or_airboundary_dict = (
            self.subsurface_dict | self.airboundary_dict
        )
        self.subsurface_or_airboundary_names = list(
            self.subsurface_or_airboundary_dict.keys()
        )

        data_arr = filter_data_arr(data_arr_, self.subsurface_or_airboundary_names)

        bar, cmap, norm = flow_colorbar(abs(data_arr.values), self.axes)
        normalized_absolute_values = [norm(abs(i)) for i in data_arr.values]
        value_signs = [int(math.copysign(1, i)) for i in data_arr.values]
        styles = [
            ConnectionStyles().afn_with_data(color=cmap(i), linewidth=i * WIDTH_FACTOR)
            for i in normalized_absolute_values
        ]

        subsurfaces_or_airboundaries = [
            self.subsurface_or_airboundary_dict[i] for i in data_arr.space_names.values
        ]

        _, lines = add_connection_lines(
            [i.domain for i in subsurfaces_or_airboundaries],
            [i.edge for i in subsurfaces_or_airboundaries],
            self.zones,
            calculate_cardinal_points(self.cardinal_domain),
            styles,
            self.axes,
        )
        add_arrows(
            lines,
            value_signs,
            np.array(normalized_absolute_values) / ARROW_FACTOR,
            self.axes,
            colors=[cmap(i) for i in normalized_absolute_values],
        )

        # print(subsurfaces)
        return self
