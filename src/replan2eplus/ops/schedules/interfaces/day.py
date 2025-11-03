from dataclasses import dataclass
from datetime import time

from typing import NamedTuple

import numpy as np
from utils4plans.lists import pairwise
from replan2eplus.ops.schedules.interfaces.constants import (
    DAY_START_TIME,
    DAY_END_TIME,
    MINUTES_PER_DAY,
)
import xarray as xr
from xarray_schema import DataArraySchema

from replan2eplus.ops.schedules.interfaces.utils import create_datetime


class TimeEntry(NamedTuple):
    end_time: time
    value: float


@dataclass
class Day:
    arr: xr.DataArray

    def __post_init___(self):
        schema = DataArraySchema(
            dtype=np.integer, shape=(MINUTES_PER_DAY,), dims=(("datetime",))
        )
        schema.validate(self.arr)


# TODO => this can possibly be integrated into the next function
def create_slice(t1: time, t2: time):
    return slice(create_datetime(t1), create_datetime(t2))


def update_arr(arr: xr.DataArray, t1: time, t2: time, value: float):
    slice_ = create_slice(t1, t2)
    arr.loc[dict(datetime=slice_)] = value
    return arr


def initialize_array(stime: time, etime: time):
    tix = xr.date_range(
        create_datetime(stime),
        create_datetime(etime),
        freq="min",
    )

    arr = xr.DataArray(np.zeros(shape=(MINUTES_PER_DAY)), coords={"datetime": tix})
    return arr


def create_day_from_single_value(
    value: float,
    stime: time = DAY_START_TIME,
    etime: time = DAY_END_TIME,
):
    arr = initialize_array(stime, etime)
    arr.data[:] = value
    return Day(arr)


def create_day_from_time_entries(
    time_entries: list[TimeEntry],
    stime: time = DAY_START_TIME,
    etime: time = DAY_END_TIME,
):
    arr = initialize_array(stime, etime)
    for ix, (i, j) in enumerate(pairwise(time_entries)):
        if ix == 0:
            arr = update_arr(arr, stime, i.end_time, i.value)

        arr = update_arr(arr, i.end_time, j.end_time, j.value)

    return Day(arr)
