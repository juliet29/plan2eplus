from dataclasses import dataclass
from datetime import date
from typing import NamedTuple
from replan2eplus.ops.schedules.interfaces.constants import HOURS_PER_DAY, DAYS_PER_YEAR
from replan2eplus.ops.schedules.interfaces.day import Day
from utils4plans.sets import set_difference
import numpy as np
from pathlib import Path


def get_index_of_date(month: int, day: int):
    # TODO write a test for this!
    DEFAULT_YEAR = 2000
    date_ = date(DEFAULT_YEAR, month, day)
    init_date = date(date_.year, 1, 1)
    return date_.toordinal() - init_date.toordinal()


class DayEntry(NamedTuple):
    month: int
    day: int
    value: Day


# NOTE: there are many ways to define a year.. at the end of the day what is most important is that we have a csv with the correct number of values.. 
# so mybe the below is a function .. 

@dataclass
class Year: # TODO -> turn this into a fx, first variable is the default day.. 
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

    def write_to_file(self, path: Path):
        # TODO should end in .csv? config for identifiable name..
        np.savetxt(
            path,
            self.array,
            # newline=",",
            delimiter=",",
            fmt="%.2f",
            header="values",
        )
