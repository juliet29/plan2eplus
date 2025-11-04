from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import NamedTuple

import numpy as np
import xarray as xr
from utils4plans.lists import pairwise
from xarray_schema import DataArraySchema

from replan2eplus.ops.schedules.interfaces.constants import (
    DAY_END_TIME,
    DAY_START_TIME,
    END_DATE,
    MINUTES_PER_YEAR,
    START_DATE,
    YEAR,
)
from replan2eplus.ops.schedules.interfaces.day import Day, create_datetime


class Date(NamedTuple):
    month: int
    day: int
    year: int = YEAR

    @property
    def python_date(self):
        return date(self.year, self.month, self.day)

    @classmethod
    def from_date(cls, date_: date):
        return cls(date_.month, date_.day)


class DayEntry(NamedTuple):
    end_date: Date
    value: Day


@dataclass
class Year:
    arr: xr.DataArray

    def __post_init__(self):
        schema = DataArraySchema(
            dtype=np.float64, shape=(MINUTES_PER_YEAR,), dims=(("datetime",))
        )
        schema.validate(self.arr)

    def write_to_file(self, path: Path):
        # TODO should end in .csv? config for identifiable name..
        np.savetxt(
            path,
            self.arr,
            # newline=",",
            delimiter=",",
            fmt="%.2f",
            header="values",
        )


def initialize_year_array():
    start_datetime = create_datetime(DAY_START_TIME, START_DATE)
    end_datetime = create_datetime(DAY_END_TIME, END_DATE)

    tix = xr.date_range(start_datetime, end_datetime, freq="min")

    arr = xr.DataArray(np.zeros(shape=(MINUTES_PER_YEAR)), coords={"datetime": tix})
    return arr


def update_year_arr(arr: xr.DataArray, day1: Date, day2: Date, value: Day):
    slice_ = slice(
        create_datetime(DAY_START_TIME, day1.python_date),
        create_datetime(DAY_END_TIME, day2.python_date),
    )

    for date_, group in arr.loc[dict(datetime=slice_)].groupby("datetime.date"):
        arr.loc[dict(datetime=group.datetime)] = value.arr.data

    return arr


def create_year_from_day_entries(day_entries: list[DayEntry]):
    # TODO to ensure that last entry is 12/31...
    arr = initialize_year_array()
    for ix, (i, j) in enumerate(pairwise(day_entries)):
        if ix == 0:
            arr = update_year_arr(arr, Date.from_date(START_DATE), i.end_date, i.value)

        arr = update_year_arr(arr, i.end_date, j.end_date, j.value)

    return Year(arr)


