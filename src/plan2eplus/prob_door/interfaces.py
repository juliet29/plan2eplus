from dataclasses import dataclass
from datetime import date, time, timedelta
from enum import Enum
from typing import NamedTuple
from numpy.random import Generator, PCG64
import numpy as np
from rich import print
from scipy.stats import geom
from tabulate import tabulate

from plan2eplus.ops.schedules.interfaces.constants import DAY_END_TIME
from plan2eplus.ops.schedules.interfaces.day import TimeEntry as BaseTimeEntry
from plan2eplus.paths import SEED

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
    generator: Generator = Generator(PCG64(SEED))
    # TODO here can possibly add seed.. -> maybe want a different seed for each day?, and each interval.., so somewhere high up, when are creating the year...

    @property
    def distribution(self):
        scipy_random_generator = geom
        scipy_random_generator.random_state = self.generator
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
    generator: Generator

    @property
    def X_open(self):
        return GeometricDisribution(self.p_open, self.generator)

    @property
    def X_close(self):
        return GeometricDisribution(self.p_close, self.generator)


# TODO test this!


class VentingInput(NamedTuple):
    day_p_open: float
    day_p_close: float

    night_p_open: float
    night_p_close: float

    early_morning_end: time
    night_start: time


default_venting_input = VentingInput(
    # NOTE: could imagine having different distributions for different kinds of rooms,
    # NOTE: limitation in that the minimum interval here is 15 minutes
    # More likely to open the door during the day, and likely to leave it open for a longer period of time
    day_p_open=0.5,
    day_p_close=0.7,
    # Unlikely to open door, but if do, likely to close again within a short interval
    night_p_open=0.1,
    night_p_close=0.99,
    early_morning_end=time(6, 0),
    night_start=time(21, 0),
)


class DistributionAndTime(NamedTuple):
    distribution: Distributions
    end_time: time


@dataclass
class SingleDayVentingAssignment:
    generator: Generator
    input: VentingInput = default_venting_input

    @property
    def daytime_distribution(self):
        return Distributions(self.input.day_p_open, self.input.day_p_close, self.generator)

    @property
    def nightime_distribution(self):
        return Distributions(
            self.input.night_p_open, self.input.night_p_close, self.generator
        )

    @property
    def early_morning(self):
        return DistributionAndTime(
            self.nightime_distribution, self.input.early_morning_end
        )

    @property
    def day(self):
        return DistributionAndTime(self.daytime_distribution, self.input.night_start)

    @property
    def night(self):
        return DistributionAndTime(self.nightime_distribution, DAY_END_TIME)


# class DefaultDistributions:
#     # TODO should also have some info about the times?
#     day: Distributions = Distributions(
#         p_open=0.5, p_close=0.7
#     )  # more likely to open the door during the day, and likely to leave it open for a longer period of time
#     night: Distributions = Distributions(
#         p_open=0.1, p_close=0.99
#     )  # Unlikely to open door, but if do, likely to close again within a short interval
#     # could imagine having different distributions for different kinds of rooms,
#     # limitation in that the minimum interval here is 15 minutes


# class TimesAssign:
#     early_morning = DistributionAndTime(DefaultDistributions.night, time(6, 0))
#     day = DistributionAndTime(DefaultDistributions.day, time(21, 0))
#     night = DistributionAndTime(DefaultDistributions.night, time(23, 59))

# print(f"{base_time_entries=}\n")
# print(f"{day=}\n")
# print(f"{night=}\n")
# print(f"{nice_combo=}\n")

# print(operating_entries)
