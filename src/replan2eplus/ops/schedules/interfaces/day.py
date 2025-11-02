from dataclasses import dataclass
from datetime import time

from typing import NamedTuple

import numpy as np
from utils4plans.lists import pairwise
from replan2eplus.ops.schedules.interfaces.constants import (
    HOURS_PER_DAY,
    LEN_INTERVAL,
    MINUTES_PER_HOUR,
    N_INTERVALS_PER_HOUR,
)
import xarray as xr


class TimeEntryHours(NamedTuple):
    end_hour: int
    value: float


@dataclass
class Day:
    time_entries: list[TimeEntryHours]

    def __post_init__(self):
        assert self.time_entries[-1].end_hour == HOURS_PER_DAY, (
            "Need the last entry to end at 24"
        )

    @classmethod
    def from_single_value(cls, value: float):
        return cls([TimeEntryHours(HOURS_PER_DAY, value)])

    @property
    def array(self):
        if len(self.time_entries) == 1:
            return np.full(shape=(HOURS_PER_DAY), fill_value=self.time_entries[0].value)

        arr = np.zeros(24)
        for ix, (i, j) in enumerate(pairwise(self.time_entries)):
            if ix == 0:
                arr[0 : i.end_hour] = i.value

            arr[i.end_hour : j.end_hour] = j.value
        return arr


# NOTE: skipping weeks interface, assuming things are constant or just a few days..
# if had to do a week inteface, would expect different behavior..


class TimeEntry(NamedTuple):
    end_time: time
    value: float


def xarray_day():
    hours = range(0, HOURS_PER_DAY)
    minutes = range(0, MINUTES_PER_HOUR)
    dims = ["hours", "minutes"]
    data = np.zeros(shape=(HOURS_PER_DAY, MINUTES_PER_HOUR))
    return xr.DataArray(data, coords=([hours, minutes]), dims=dims)
