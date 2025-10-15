from typing import NamedTuple
from dataclasses import dataclass
from utils4plans.lists import pairwise
import numpy as np
from datetime import date

from utils4plans.sets import set_difference

# TODO move to config
HOURS_PER_DAY = 24
DAYS_PER_YEAR = 365


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


def get_index_of_date(month: int, day: int):
    DEFAULT_YEAR = 2000
    date_ = date(DEFAULT_YEAR, month, day)
    init_date = date(date_.year, 1, 1)
    return date_.toordinal() - init_date.toordinal()


class DayEntry(NamedTuple):
    month: int
    day: int
    value: Day


# NOTE: skipping weeks interface, assuming things are constant or just a few days..
# if had to do a week inteface, would expect different behavior.. 

@dataclass
class Year:
    default_day: Day
    day_entries: list[DayEntry]
    # TODO from single entry -> return constant ..

    @property
    def array(self):
        year = np.zeros(shape=(DAYS_PER_YEAR, HOURS_PER_DAY))
        date_indices = [get_index_of_date(i.month, i.day) for i in self.day_entries]
        default_indices = set_difference(range(DAYS_PER_YEAR), date_indices)

        for date_ix, entry in zip(date_indices, self.day_entries):
            year[date_ix] = entry.value.array

        for date_ix in default_indices:
            year[date_ix] = self.default_day.array

        return year.flatten()
    
    def write_to_file(self):
        pass
