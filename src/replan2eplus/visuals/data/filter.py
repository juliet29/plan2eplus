import xarray as xr
from expression.collections import Seq
from replan2eplus.geometry.directions import WallNormalLiteral
from typing import get_args
from utils4plans.sets import set_difference, set_intersection


def filter_data_arr(data_arr: xr.DataArray, geom_names: list[str]):
    space_names_to_compare = data_arr.space_names.values  # TODO replace..
    diff = set_difference(space_names_to_compare, geom_names)
    if diff:
        intersect = set_intersection(space_names_to_compare, geom_names)

        assert (
            intersect
        ), f"Some space_names are not contained in the expected geometry, and there is no intersection! -> {diff}. "
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


def handle_external_node_data(data_arr_: xr.DataArray):
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
