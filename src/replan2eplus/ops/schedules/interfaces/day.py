from dataclasses import dataclass

from typing import NamedTuple

import numpy as np
from utils4plans.lists import pairwise
from replan2eplus.ops.schedules.interfaces.constants import HOURS_PER_DAY


class TimeEntry(NamedTuple):
    end_hour: int
    value: float


@dataclass
class Day:
    time_entries: list[TimeEntry]

    def __post_init__(self):
        assert self.time_entries[-1].end_hour == HOURS_PER_DAY, (
            "Need the last entry to end at 24"
        )

    @classmethod
    def from_single_value(cls, value: float):
        return cls([TimeEntry(HOURS_PER_DAY, value)])

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

