from dataclasses import dataclass
from enum import StrEnum
from typing import NamedTuple, Literal
from ladybug.datacollection import BaseCollection
import polars as pl
import numpy as np
import xarray as xr
from datetime import datetime

from replan2eplus.idfobjects.idf import AnalysisPeriod


SpaceTuple = NamedTuple("SpaceTuple", [("name", str), ("space_type", str)])


class SpaceTypes(StrEnum):
    SYSTEM = "System"
    ZONE = "Zone"
    SURFACE = "Surface"
    SITE = "Site"


SpaceTypesLiteral = Literal["System", "Zone", "Surface", "Site"]


def get_name_for_spatial_data(dataset: BaseCollection):
    keys = dataset.header.metadata.keys()
    space_types = [i.value for i in SpaceTypes]
    # print(keys)
    for i in space_types:
        if i in keys:
            # TODO should have a typed dict for the metadata?
            return SpaceTuple(dataset.header.metadata[i], i)
    else:
        raise Exception(f"Spatial type is not defined: {keys}")


@dataclass
class SQLCollection:
    collection: BaseCollection

    @property
    def values(self):
        return self.collection.values

    @property
    def datetimes(self):
        return self.collection.datetimes

    @property
    def qoi(self):
        return self.collection.header.metadata["type"]

    @property
    def unit(self):
        return self.collection.header.unit

    @property
    def analysis_period(self):
        return self.collection.header.analysis_period

    @property
    def space_tuple(self):
        return get_name_for_spatial_data(self.collection)

    @property
    def space_name(self):
        return self.space_tuple.name

    @property
    def space_type(self):
        return self.space_tuple.space_type





class DFC:
    """Dataframe Columns"""

    # CASE_NAMES = "case_names"
    SPACE_NAMES = "space_names"

    DATETIMES = "datetimes"
    HOUR = "hour"
    TIME = "time"

    # ZONE = "zone"
    # DIRECTION = "direction"
    # IS_EXTERIOR = "is_exterior"

    # # after pivoting for altair
    # VARIABLE = "variable"
    # VALUE = "value"


@dataclass
class QOIResult:
    qoi: str
    unit: str  # TODO units literal..
    analysis_period: AnalysisPeriod
    space_type: SpaceTypesLiteral
    data_arr: xr.DataArray

    def __post_init__(self):
        assert set(self.data_arr.dims) == set([DFC.DATETIMES, DFC.SPACE_NAMES])

    @classmethod
    def from_sql_collections(cls, collections: list[SQLCollection]):
        return cls(*sqlcollections_to_qoi_result(collections))

    @property
    def datetimes(self):
        return list(self.data_arr.coords[DFC.DATETIMES].values)

    @property
    def space_names(self):
        return list(self.data_arr.coords[DFC.SPACE_NAMES].values)

    def check_can_compute(self, other):
        if not isinstance(other, QOIResult):
            raise Exception(
                f"{other} is not of type QOIResult"
            )  # TODO define a higher level exception here..
        assert self.datetimes == other.datetimes
        assert self.space_names == other.space_names
        assert self.unit == other.unit
        return other

    def copy_with_new_arr(self, result: xr.DataArray):
        return QOIResult(self.qoi, self.unit, self.analysis_period, self.space_type, result)

    def __sub__(self, other):
        other = self.check_can_compute(other)
        result = self.data_arr - other.data_arr
        return self.copy_with_new_arr(result)

    def __add__(self, other):
        other = self.check_can_compute(other)
        result = self.data_arr + other.data_arr
        return self.copy_with_new_arr(result)
    



def data_arr_from_sqlcollections(
    datetimes: list[datetime], space_names: list[str], collections: list[SQLCollection]
):
    coords = [list(datetimes), space_names]
    dims = [DFC.DATETIMES, DFC.SPACE_NAMES]
    data = np.array([i.values for i in collections]).transpose()
    return xr.DataArray(data=data, coords=coords, dims=dims)


def check_is_unique(items: list):
    unique_items = set(items)
    assert len(unique_items) == 1, (
        f"There is more than one type of item! {unique_items}"
    )
    return list(unique_items)[0]

def sqlcollections_to_qoi_result(collections: list[SQLCollection]):
    qoi = check_is_unique([i.qoi for i in collections])
    unit = check_is_unique([i.unit for i in collections])
    space_type = check_is_unique(
        [i.space_type for i in collections]
    )  # TODO this may also fail.. on failure, split
    analysis_period = check_is_unique([i.analysis_period for i in collections])

    datetimes = check_is_unique([i.datetimes for i in collections])

    # space_names = [i.space_name for i in collections]
    valid_collections = [i for i in collections if len(i.values) > 0]
    valid_space_names = [i.space_name for i in valid_collections]

    data_arr = data_arr_from_sqlcollections(
        datetimes, valid_space_names, valid_collections
    )

    return (qoi, unit, analysis_period, space_type, data_arr)


# def sqlcollections_to_qoi_result(collections: list[SQLCollection]):
#     pass
