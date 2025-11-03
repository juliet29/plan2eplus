from dataclasses import dataclass
from rich import print
from xarray_schema import DataArraySchema
from utils4plans.lists import pairwise
from datetime import date, datetime
from typing import NamedTuple
from replan2eplus.ops.schedules.interfaces.constants import (
    DAY_START_TIME,
    END_DATE,
    HOURS_PER_DAY,
    DAYS_PER_YEAR,
    MINUTES_PER_DAY,
    MINUTES_PER_YEAR,
    START_DATE,
    DAY_END_TIME,
    YEAR,
)
from replan2eplus.ops.schedules.interfaces.day import Day, create_datetime
from utils4plans.sets import set_difference
import numpy as np
from pathlib import Path
import xarray as xr


# TODO this becomes irrelevant if use xarray..
def get_index_of_date(month: int, day: int):
    # TODO write a test for this!
    DEFAULT_YEAR = 2000
    date_ = date(DEFAULT_YEAR, month, day)
    init_date = date(date_.year, 1, 1)
    return date_.toordinal() - init_date.toordinal()


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
    # print(day1, day2)
    slice_ = slice(
        create_datetime(DAY_START_TIME, day1.python_date),
        create_datetime(DAY_END_TIME, day2.python_date),
    )
    ar1 = arr.loc[dict(datetime=slice_)]

    # def replace(group):
    #     return value.arr

    for name, group in ar1.groupby("datetime.date"):
        arr.loc[dict(datetime=group.datetime)] = value.arr.data

    # ar2 = ar1.groupby("datetime.time").map(replace)
    # print(ar2.datetime)
    # print(ar1.datetime)
    # arr.loc[dict(datetime=slice_)] = ar2
    # print(arr.data)
    # print(arr.shape)

    return arr


def create_year_from_day_entries(day_entries: list[DayEntry]):
    # TODO to ensure that last entry is 12/31...
    arr = initialize_year_array()
    for ix, (i, j) in enumerate(pairwise(day_entries)):
        if ix == 0:
            arr = update_year_arr(arr, Date.from_date(START_DATE), i.end_date, i.value)

        arr = update_year_arr(arr, i.end_date, j.end_date, j.value)

    return Year(arr)


# @dataclass
# class Year2:  # TODO -> turn this into a fx, first variable is the default day..
#     default_day: Day
#     day_entries: list[DayEntry]
#     # TODO from single entry -> return constant ..

#     @property
#     def array(self):
#         year = np.zeros(shape=(DAYS_PER_YEAR, MINUTES_PER_DAY))
#         date_indices = [get_index_of_date(i.month, i.day) for i in self.day_entries]
#         default_indices = set_difference(range(DAYS_PER_YEAR), date_indices)

#         for date_ix, entry in zip(date_indices, self.day_entries):
#             year[date_ix] = entry.value.arr

#         for date_ix in default_indices:
#             year[date_ix] = self.default_day.arr

#         return year.flatten()

#     def write_to_file(self, path: Path):
#         # TODO should end in .csv? config for identifiable name..
#         np.savetxt(
#             path,
#             self.array,
#             # newline=",",
#             delimiter=",",
#             fmt="%.2f",
#             header="values",
#         )
