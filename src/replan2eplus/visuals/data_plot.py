from dataclasses import dataclass
from replan2eplus.ezobjects.afn import set_difference, set_intersection
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.visuals.base_plot import BasePlot
from replan2eplus.visuals.transformations import (
    EXPANSION_FACTOR,
)
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.visuals.axis_modifications import (
    AnnotationPair,
    add_annotations,
    add_connection_lines,
    add_rectangles,
    add_surface_lines,
)
from replan2eplus.visuals.organization import (
    organize_connections,
    organize_subsurfaces_and_surfaces,
)
from replan2eplus.visuals.styles.artists import (
    AnnotationStyles,
    ConnectionStyles,
    RectangleStyles,
    SurfaceStyles,
)
from replan2eplus.results.collections import DFC
import xarray as xr

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib as mpl
from matplotlib.axes import Axes
from xarray import DataArray
from typing import Iterable


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


@dataclass
class DataForPlot:
    space_names: list[str]
    values: list[float]

    # potentially denumpy-ify..

    # TODO these need to be aligned! no checks on this but maybe can use xarray!


def filter_data_arr(data_arr: DataArray, geom_names: list[str]):
    space_names_to_compare = data_arr.space_names.values  # TODO replace..
    diff = set_difference(space_names_to_compare, geom_names)
    if diff:
        intersect = set_intersection(space_names_to_compare, geom_names)

        assert intersect, (
            f"Some space_names are not contained in the expected geometry, and there is not intersection! -> {diff}. "
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

    def plot_zones_with_data(self, data_arr_: DataArray):
        data_arr = filter_data_arr(data_arr_, self.zone_names)
        bar, cmap, norm = pressure_colorbar(data_arr.values, self.axes)
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
        self, data_arr_: DataArray, subsurfaces: list[Subsurface]
    ):
        # TODO include surfaces which are airboundaries.. 
        self.subsurface_dict =  {i.subsurface_name.upper(): i for i in subsurfaces}
        self.subsurface_names = list(self.subsurface_dict.keys())

        data_arr = filter_data_arr(data_arr_, self.subsurface_names)

        bar, cmap, norm  = flow_colorbar(data_arr.values, self.axes)
        styles = [ConnectionStyles().afn_with_data(color=cmap(norm(i))) for i in data_arr.values]

        subsurfaces = [self.subsurface_dict[i] for i in data_arr.space_names.values]

        add_connection_lines([i.domain for i in subsurfaces], [i.edge for i in subsurfaces], self.zones, self.cardinal_domain.cardinal, styles, self.axes)
    
        # print(subsurfaces)
        return self
