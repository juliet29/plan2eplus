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


def check_is_unique(items: list):
    unique_items = set(items)
    assert len(unique_items) == 1, (
        f"There is more than one type of item! {unique_items}"
    )
    return list(unique_items)[0]


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

def sqlcollections_to_qoi_result(collections: list[SQLCollection]):
    pass


@dataclass
class QOIResult2:
    qoi: str
    unit: str # TODO units literal.. 
    space_type: SpaceTypesLiteral
    # analysis_period: AnalysisPeriod
    data_arr: xr.DataArray
    # space_names: list[str]
    # datetimes: list[datetime]

    # post init -> check that the dimensions of the data arrary.. 




@dataclass
class QOIResult:
    collections: list[SQLCollection]

    # @classmethod
    # def from_collections(cls, collections: )

    # post init checking that all these things are the same..
    # TODO going to need to be able to initialize this another way.. 
    def __post_init__(self):
        self.qoi = check_is_unique([i.qoi for i in self.collections])
        self.unit = check_is_unique([i.unit for i in self.collections])
        self.space_type = check_is_unique(
            [i.space_type for i in self.collections]
        )  # TODO this may also fail.. on failure, split
        self.analysis_period = check_is_unique(
            [i.analysis_period for i in self.collections]
        )  # TODO this may fail.. unless enforce the rule when setting the analysis periods.. or ask to specify when reading SQL..
        self.datetimes = check_is_unique([i.datetimes for i in self.collections])

        self.space_names = [i.space_name for i in self.collections]
        self.valid_collections = [i for i in self.collections if len(i.values) > 0]
        self.valid_space_names = [i.space_name for i in self.valid_collections]

        # TODO when create new QOIResult from a sum, do we still do the post init?

    @property
    def data_dict(self):
        data_dict_ = {}
        data_dict_[DFC.DATETIMES] = self.datetimes
        for collection in self.valid_collections:
            data_dict_[collection.space_name] = collection.values

        return data_dict_

    @property
    def data_arr(self):
        coords = [list(self.datetimes), self.valid_space_names]
        dims = [DFC.DATETIMES, DFC.SPACE_NAMES]
        data = np.array([i.values for i in self.valid_collections]).transpose()
        # print(data)
        arr = xr.DataArray(
            data=data,  coords=coords, dims=dims
        )
        return arr # TODO my custom xarr that i define methods on? or just a function thats for plotting.. 

    @property
    def dataframe(self):
        return pl.DataFrame(self.data_dict)

    # TODO try out xarray.. -> nice because has an index..

    def __add__(self, other):
        if not isinstance(other, QOIResult):
            raise Exception(f"{other} is not of type QOIResult") # TODO define a higher level exception here.. 
        assert self.datetimes == other.datetimes
        assert self.space_names == other.space_names
        assert self.unit == other.unit
        return self.data_arr + other.data_arr

    # property -> filtered collections -> only values that are non zero..
    # space names.. that are non zero..

    # doing operations on these..
    # qoi ..
