from dataclasses import dataclass
from utils4plans.lists import pairwise
from typing import NamedTuple
from enum import Enum
from datetime import time, timedelta, datetime, date
from scipy.stats import geom
import numpy as np
from rich import print
from tabulate import tabulate
from replan2eplus.ops.schedules.interfaces.day import TimeEntry as BaseTimeEntry

from replan2eplus.ops.schedules.interfaces.day import (
    Day,
    create_day_from_single_value,
    create_day_from_time_entries,
)
from replan2eplus.ops.schedules.interfaces.year import DayEntry, Date
from replan2eplus.ops.schedules.interfaces.utils import create_datetime
import xarray as xr
from replan2eplus.ops.schedules.interfaces.constants import DAY_END_TIME, DAY_START_TIME
import numpy as np 

# TODO CONNECT TO CONFIG RELATED TO NUMBER OF TIMESTEPS
LEN_INTERVAL = timedelta(minutes=15)
DEFAULT_FAKE_DATE = date(2025, 1, 1)


class VentingState(Enum):
    CLOSE = 0
    OPEN = 1


class TimeEntry(
    NamedTuple
):  # TODO consider this an extension of the original time entry, and have a mechanism for converting back to it
    time: time
    value: VentingState

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TimeEntry):
            return (self.time == other.time) and (self.value == other.value)
        raise Exception  # TODO make a repo wide error for this

    def __hash__(self) -> int:
        return hash(self.time) + hash(self.value)

    @property
    def base_time_entry(self):
        return BaseTimeEntry(self.time, self.value.value)


@dataclass
class TimeEntryList:
    values: list[TimeEntry]

    @property
    def last(self):
        return self.values[-1]

    def append(self, entry: TimeEntry):
        self.values.append(entry)

    @property
    def unique_and_sorted(self):
        return sorted(set(self.values), key=lambda x: x.time)

    # @property
    # def last_time(self):
    #     pass


class GeometricDisribution(NamedTuple):
    probability_of_success: float
    # TODO here can possibly add seed.. -> maybe want a different seed for each day?, and each interval.., so somewhere high up, when are creating the year...

    @property
    def distribution(self):
        return geom(self.probability_of_success)

    def sample(self) -> int:
        return self.distribution.rvs()

    @property
    def probability_mass_function(self):
        print(f"prob of success: {self.probability_of_success:.2%}")
        min_prob = 0.01
        max_prob = 0.99
        possible_outcomes = np.arange(
            self.distribution.ppf(min_prob), self.distribution.ppf(max_prob)
        )
        probabilities = [self.distribution.pmf(i) for i in possible_outcomes]  # pyright: ignore[reportAttributeAccessIssue]
        data = [(x, f"{p:.2%}") for x, p in zip(possible_outcomes, probabilities)]
        if len(data) > 8:
            data = data[0:7]
        print(tabulate(data))
        # TODO -> would be nice to put this in a nice table..

    @property
    def stats(self):
        print(self.distribution.stats())

    def show_summary(self, time_interval=LEN_INTERVAL):
        mean, variance = self.distribution.stats()
        m = (time_interval * mean).seconds // 60
        v = (time_interval * variance).seconds // 60
        print(f"prob of success: {self.probability_of_success}")
        print(
            f"On average, a changeover will occur after {m} minutes, with a variance of {v} minutes"
        )


class Distributions(NamedTuple):
    p_open: float
    p_close: float

    @property
    def X_open(self):
        return GeometricDisribution(self.p_open)

    @property
    def X_close(self):
        return GeometricDisribution(self.p_close)


def get_next_time(
    init_time_: time, dist: GeometricDisribution, len_interval: timedelta = LEN_INTERVAL
) -> time:
    init_time = datetime.combine(DEFAULT_FAKE_DATE, init_time_)

    n_intervals = dist.sample()
    next_datetime = init_time + n_intervals * len_interval
    return next_datetime.time()


# TODO test this!


def is_crossing_midnight(tprev: time, tnext: time):
    if tprev > tnext:
        return True
    return False


def create_time_entries(
    start_value: VentingState,
    start_time: time,  # TOOD could be a time entry ..
    end_time: time,
    distributions: Distributions,
):
    entries = TimeEntryList([TimeEntry(start_time, start_value)])
    count = 0
    MAX_COUNT = 100

    # create disctr

    while entries.last.time < end_time:
        match entries.last.value:
            case VentingState.OPEN:
                next_time = get_next_time(
                    entries.last.time,
                    distributions.X_close,
                )
                next_entry = TimeEntry(next_time, VentingState.CLOSE)

            case VentingState.CLOSE:
                next_time = get_next_time(entries.last.time, distributions.X_open)
                next_entry = TimeEntry(next_time, VentingState.OPEN)

            case _:
                raise Exception(f"Invalid Venting State: {entries.last.value}")

        if next_entry.time > end_time or is_crossing_midnight(
            entries.last.time, next_entry.time
        ):
            next_entry = TimeEntry(end_time, next_entry.value)
            entries.append(next_entry)
            break

        entries.append(next_entry)

        count += 1
        if count > MAX_COUNT:
            raise Exception(f"Exceeded max count: current entries {entries.values}")
    return entries


class DefaultDistributions:
    # TODO should also have some info about the times?
    day: Distributions = Distributions(
        p_open=0.5, p_close=0.7
    )  # more likely to open the door during the day, and likely to leave it open for a longer period of time
    night: Distributions = Distributions(
        p_open=0.1, p_close=0.99
    )  # Unlikely to open door, but if do, likely to close again within a short interval
    # could imagine having different distributions for different kinds of rooms,
    # limitation in that the minimum interval here is 15 minutes


class Times(NamedTuple):
    distribution: Distributions
    end: time


class TimesAssign:
    early_morning = Times(DefaultDistributions.night, time(6, 0))
    day = Times(DefaultDistributions.day, time(21, 0))
    night = Times(DefaultDistributions.night, time(23, 59))


def create_day_entries(start_value=VentingState.CLOSE, assn=TimesAssign()):
    start_time = time(0, 0)
    early_morning = create_time_entries(
        start_value, start_time, assn.early_morning.end, assn.early_morning.distribution
    )
    day = create_time_entries(
        early_morning.last.value,
        early_morning.last.time,
        assn.day.end,
        assn.day.distribution,
    )

    night = create_time_entries(
        day.last.value,
        day.last.time,
        assn.night.end,
        assn.night.distribution,
    )

    combined = TimeEntryList(
        early_morning.values + day.values + night.values
    ).unique_and_sorted

    assert combined[0].time == time(0, 0)
    assert combined[-1].time == time(23, 59)

    base_time_entries = [i.base_time_entry for i in combined]

    # print(sum([i.value for i in base_time_entries]))
    return base_time_entries

    # print(f"{base_time_entries=}\n")
    # print(f"{day=}\n")
    # print(f"{night=}\n")
    # print(f"{nice_combo=}\n")


def create_year():
    closed_day = create_day_from_single_value(VentingState.CLOSE.value)
    pre_range = xr.date_range()
    operating_range = xr.date_range(
        create_datetime(DAY_START_TIME, Date(5, 1).python_date),
        create_datetime(DAY_END_TIME, Date(8, 1).python_date),
        freq="D",
    )
    operating_entries = []

    start_value = VentingState.CLOSE

    for i in operating_range.date:  # pyright: ignore[reportAttributeAccessIssue]
        entries = create_day_entries(start_value)
        day = create_day_from_time_entries(entries)
        operating_entries.append(DayEntry(Date.from_date(i), day))
        start_value = VentingState(entries[-1].value)

    # print(operating_entries)
