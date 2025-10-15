from typing import NamedTuple
from dataclasses import dataclass
from utils4plans.lists import pairwise
import numpy as np

# TODO move to config
HOURS_PER_DAY = 24


class Time(NamedTuple):
    start_hour: int
    end_hour: int
    value: float

    # TODO post init end_hour should be between 1 and 24, start_hour is between 0 and 23..


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

    def create_array(self):
        if len(self.time_entries) == 1:
            i = self.time_entries[0]
            return np.full(shape=(HOURS_PER_DAY), fill_value=i.value)

        arr = np.zeros(24)
        for ix, (i, j) in enumerate(pairwise(self.time_entries)):
            if ix == 0:
                arr[0 : i.end_hour] = i.value

            arr[i.end_hour : j.end_hour] = j.value
        return arr
    
class Year:
    
