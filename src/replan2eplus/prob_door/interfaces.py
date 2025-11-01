from dataclasses import dataclass
from typing import NamedTuple
from enum import Enum
from datetime import time, timedelta, datetime, date
from scipy.stats import geom


class VentingState(Enum):
    CLOSE = 0
    OPEN = 1


class TimeEntry(
    NamedTuple
):  # TODO consider this an extension of the original time entry, and have a mechanism for converting back to it
    time: time
    value: VentingState


@dataclass
class TimeEntryList:
    values: list[TimeEntry]

    @property
    def last(self):
        return self.values[-1]

    def append(self, entry: TimeEntry):
        self.values.append(entry)

    # @property
    # def last_time(self):
    #     pass


class GeometricDisribution(NamedTuple):
    probability_of_success: float
    # TODO here can possibly add seed..

    @property
    def distribution(self):
        return geom(self.probability_of_success)

    def sample(self) -> int:
        return self.distribution.rvs()


class Distributions(NamedTuple):
    p_open: float
    p_close: float

    @property
    def X_open(self):
        return GeometricDisribution(self.p_open)

    @property
    def X_close(self):
        return GeometricDisribution(self.p_open)


# TODO CONNECT TO CONFIG RELATED TO NUMBER OF TIMESTEPS
LEN_INTERVAL = timedelta(minutes=15)
DEFAULT_FAKE_DATE = date(2025, 1, 1)


def get_next_time(
    init_time_: time, dist: GeometricDisribution, len_interval: timedelta = LEN_INTERVAL
) -> time:
    init_time = datetime.combine(DEFAULT_FAKE_DATE, init_time_)

    n_intervals = dist.sample()
    next_datetime = init_time + n_intervals * len_interval
    return next_datetime.time()


# TODO test this!


def create_time_entries(
    start_value: VentingState,
    start_time: time,  # TOOD could be a time entry ..
    end_time: time,
    distributions: Distributions,
):
    entries = TimeEntryList([TimeEntry(start_time, start_value)])
    count = 0
    MAX_COUNT = 10

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

        entries.append(next_entry)

        count += 1
        if count > MAX_COUNT:
            raise Exception("Exceeded max count")
