from dataclasses import dataclass
import matplotlib.pyplot as plt
from datetime import date, timedelta
from pathlib import Path
from typing import NamedTuple

import numpy as np
import xarray as xr
from utils4plans.lists import pairwise
from xarray_schema import DataArraySchema

from replan2eplus.ops.schedules.interfaces.constants import (
    DAY_END_TIME,
    DAY_START_TIME,
    YEAR_END_DATE,
    MINUTES_PER_YEAR,
    YEAR_START_DATE,
    YEAR,
)
from replan2eplus.ops.schedules.interfaces.day import Day, create_datetime
from replan2eplus.ops.schedules.interfaces.utils import create_datetime_from_date


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

    @property
    def minus_one(self):
        dt = create_datetime_from_date(self.python_date)
        td = timedelta(days=1)
        return Date.from_date(dt - td)

    @property
    def plus_one(self):
        dt = create_datetime_from_date(self.python_date)
        td = timedelta(days=1)
        return Date.from_date(dt + td)


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
    start_datetime = create_datetime(DAY_START_TIME, YEAR_START_DATE)
    end_datetime = create_datetime(DAY_END_TIME, YEAR_END_DATE)

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


def create_partial_year_from_day_entries(day_entries: list[DayEntry]):
    arr = initialize_year_array()
    days = [i.end_date for i in day_entries] + [day_entries[-1].end_date.plus_one]
    for ix, (i, j) in enumerate(pairwise(days)):
        arr = update_year_arr(arr, i, j, day_entries[ix].value)

    return Year(arr)


def create_year_from_day_entries_and_defaults(
    day_entries: list[DayEntry], default_day: Day
):
    # assuming just ONE list of entries
    init_day = day_entries[0].end_date # TODO -> similar to prob, implement get last and get first to clean this up, ie a class for list of DayEntries
    final_day = day_entries[-1].end_date

    starting_range = (Date.from_date(YEAR_START_DATE), init_day.minus_one)
    ending_range = (final_day.plus_one, (Date.from_date(YEAR_END_DATE)))

    year = create_partial_year_from_day_entries(day_entries)

    year.arr = update_year_arr(year.arr, *starting_range, default_day)
    year.arr = update_year_arr(year.arr, *ending_range, default_day)

    return year
