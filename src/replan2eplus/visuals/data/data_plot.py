from dataclasses import dataclass
from expression.collections import Seq
from replan2eplus.geometry.directions import WallNormalLiteral
from typing import get_args

import numpy as np
from xarray import DataArray
from utils4plans.sets import set_intersection, set_difference
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
from replan2eplus.visuals.data.colorbars import (
    ColorBarFx,
    flow_colorbar,
    pressure_colorbar,
)
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


def get_matching_direction(name: str):
    for i in get_args(WallNormalLiteral):
        if i in name:
            return i


def contains_direction(name: str):
    for i in get_args(WallNormalLiteral):
        if i in name:
            return True
    return False


def handle_external_node_data(data_arr_: DataArray):
    # HERE, assuming have already selected the hour!

    da = data_arr_

    # filter array to only contain space_names that are directions, ie, contain directions.. => TODO better to filter on External Node Name, but right noe has wrong name...
    existing_space_names = da.space_names.data.tolist()

    cardinal_spaces = (
        Seq(existing_space_names).filter(lambda x: contains_direction(x)).to_list()
    )
    cardinal_da = da.sel(space_names=cardinal_spaces)

    # transform the space names to just be directions
    true_card_da = (
        cardinal_da.assign_coords(
            space_names=Seq(cardinal_da.space_names.data)
            .map(lambda x: get_matching_direction(x))
            .to_list()
        )
        .groupby("space_names")
        .mean()
    )

    return true_card_da


@dataclass
class DataPlot(BasePlot):
    zones: list[Zone]
    cardinal_expansion_factor: float = EXPANSION_FACTOR
    extents_expansion_factor: float = EXPANSION_FACTOR

    def __post_init__(self):
        super().__post_init__()
        self.zone_dict = {i.zone_name.upper(): i for i in self.zones}
        self.zone_names = [i.zone_name.upper() for i in self.zones]
        self.geom_cmap = None
        self.geom_norm = None

    def set_geometry_color_maps(
        self, data_arr_: DataArray, colorbar_fx: ColorBarFx = pressure_colorbar
    ):
        self.data_array = data_arr_
        bar, self.geom_cmap, self.geom_norm = colorbar_fx(data_arr_.values, self.axes)

    def plot_zones_with_data(self):
        assert self.geom_cmap and self.geom_norm
        data_arr = filter_data_arr(self.data_array, self.zone_names)
        print(data_arr)
        styles = [
            PolygonStyles(fill=True, color=self.geom_cmap(self.geom_norm(i)))
            for i in data_arr.values
        ]
        domains = [self.zone_dict[i].domain for i in data_arr.space_names.values]

        add_polygons(domains, styles, self.axes)

        # grey for zones not included in the data
        non_included_zones = set_difference(
            self.zone_names, data_arr.space_names.values
        )
        add_polygons(
            [self.zone_dict[i].domain for i in non_included_zones],
            [PolygonStyles(fill=True, color="gray")],
            self.axes,
        )

        return self

    def plot_cardinal_names_with_data(self):
        assert self.geom_cmap and self.geom_norm
        data_arr = handle_external_node_data(self.data_array)
        cardinal_points = calculate_cardinal_points(self.cardinal_domain)
        existing_space_names = data_arr.space_names.values

        inputs = []
        for name, location in cardinal_points.dict_.items():
            style = AnnotationStyles()
            if name in existing_space_names:
                value = data_arr.sel(space_names=name).values
                assert not value.shape  # should be individual number
                style.update_bbox_color(
                    color=self.geom_cmap(self.geom_norm(float(value)))
                )
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
            get_domains(subsurfaces_or_airboundaries),
            get_edges(subsurfaces_or_airboundaries),
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
