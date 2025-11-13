from dataclasses import dataclass
from matplotlib.colors import Colormap, Normalize

import numpy as np
from utils4plans.sets import set_difference
import xarray as xr
from replan2eplus.ops.airboundary.ezobject import Airboundary
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.zones.ezobject import Zone
from replan2eplus.geometry.contact_points import calculate_cardinal_points
from replan2eplus.visuals.axes import (
    AnnotationPair,
    AnnotationStyles,
    add_annotations,
    add_connection_lines,
    add_polygons,
)
from replan2eplus.visuals.base.base_plot import BasePlot
from replan2eplus.visuals.organize import get_domains, get_edges
from replan2eplus.visuals.styles.artists import (
    ConnectionStyles,
    PolygonStyles,
)
from replan2eplus.visuals.transforms import (
    EXPANSION_FACTOR,
)
from replan2eplus.visuals.data.arrow import add_arrows
import math
from replan2eplus.visuals.data.filter import filter_data_arr, handle_external_node_data


@dataclass
class DataPlot(BasePlot):
    zones: list[Zone]
    cardinal_expansion_factor: float = EXPANSION_FACTOR
    extents_expansion_factor: float = EXPANSION_FACTOR

    def __post_init__(self):
        super().__post_init__()
        self.zone_dict = {i.zone_name.upper(): i for i in self.zones}
        self.zone_names = [i.zone_name.upper() for i in self.zones]
        self.cmap = None
        self.norm = None

    def plot_zones_with_data(
        self, data_array: xr.DataArray, cmap: Colormap, norm: Normalize
    ):
        data_arr = filter_data_arr(data_array, self.zone_names)

        styles = [
            PolygonStyles(fill=True, color=cmap(norm(i))) for i in data_arr.values
        ]
        domains = [self.zone_dict[i].domain for i in data_arr.space_names.values]

        add_polygons(domains, styles, self.axes)

        # grey for zones not included in the d:ata
        non_included_zones = set_difference(
            self.zone_names, data_arr.space_names.values
        )
        add_polygons(
            [self.zone_dict[i].domain for i in non_included_zones],
            [PolygonStyles(fill=True, color="gray")],
            self.axes,
        )

        return self

    def plot_cardinal_names_with_data(
        self, data_array: xr.DataArray, cmap: Colormap, norm: Normalize
    ):
        data_arr = handle_external_node_data(data_array)
        cardinal_points = calculate_cardinal_points(self.cardinal_domain)
        existing_space_names = data_arr.space_names.values

        inputs = []
        for name, location in cardinal_points.dict_.items():
            style = AnnotationStyles()
            if name in existing_space_names:
                value = data_arr.sel(space_names=name).values
                assert not value.shape  # should be individual number
                style.update_bbox_color(color=cmap(norm(float(value))))
            inputs.append((name, location, style))

        add_annotations(
            [AnnotationPair(location, name) for name, location, _ in inputs],
            [style for _, _, style in inputs],
            self.axes,
        )
        return self

        # some cardinal points will not be part of the afn
        # data arr, will expect to have one variable for each thats in a typical cardinal points dict..
        # for the things that is missing, will have no color..

    def plot_connections_with_data(
        self,
        data_arr_: xr.DataArray,
        afn_surfaces: list[Subsurface | Airboundary],
        cmap: Colormap,
        norm: Normalize,
        WIDTH_FACTOR=10,
        ARROW_FACTOR=12,
    ):
        # TODO check dimensions of the dataarray..
        surface_names = [i.name.upper() for i in afn_surfaces]

        arr = filter_data_arr(data_arr_, surface_names)
        normalized_absolute_values = [norm(abs(i)) for i in arr.values]
        value_signs = [int(math.copysign(1, i)) for i in arr.values]
        styles = [
            ConnectionStyles().afn_with_data(color=cmap(i), linewidth=i * WIDTH_FACTOR)
            for i in normalized_absolute_values
        ]

        _, lines = add_connection_lines(
            get_domains(afn_surfaces),
            get_edges(afn_surfaces),
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

    def set_limits(self):
        self.axes.set_xlim(self.extents.horz_range.as_tuple)
        self.axes.set_ylim(self.extents.vert_range.as_tuple)
        return self
