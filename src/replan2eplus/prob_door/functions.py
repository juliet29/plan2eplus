from datetime import datetime, time, timedelta
from tabulate import tabulate
from rich import print

from numpy.random import Generator, PCG64
import xarray as xr
import numpy as np

from replan2eplus.ops.schedules.interfaces.constants import DAY_END_TIME, DAY_START_TIME
from replan2eplus.ops.schedules.interfaces.day import (
    create_day_from_single_value,
    create_day_from_time_entries,
)
from replan2eplus.ops.schedules.interfaces.utils import create_datetime
from replan2eplus.ops.schedules.interfaces.year import (
    Date,
    DayEntry,
    create_year_from_day_entries_and_defaults,
)
from replan2eplus.paths import SEED
from replan2eplus.prob_door.interfaces import (
    DEFAULT_FAKE_DATE,
    LEN_INTERVAL,
    BaseTimeEntry,
    DistributionAndTime,
    GeometricDisribution,
    SingleDayVentingAssignment,
    TimeEntry,
    TimeEntryList,
    VentingState,
)


def is_crossing_midnight(tprev: time, tnext: time):
    if tprev > tnext:
        return True
    return False


def get_next_time(
    init_time_: time, dist: GeometricDisribution, len_interval: timedelta = LEN_INTERVAL
) -> time:
    init_time = datetime.combine(DEFAULT_FAKE_DATE, init_time_)

    n_intervals = dist.sample()
    next_datetime = init_time + n_intervals * len_interval
    return next_datetime.time()


def create_time_entries(
    start_value: VentingState,
    start_time: time,  # TOOD could be a time entry ..
    dist_and_end_time: DistributionAndTime,
):
    distributions, end_time = dist_and_end_time
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


def create_day_entries(start_value: VentingState, generator: Generator):
    assn = SingleDayVentingAssignment(generator)
    start_time = DAY_START_TIME
    early_morning = create_time_entries(
        start_value,
        start_time,
        assn.early_morning,
    )
    day = create_time_entries(
        early_morning.last.value, early_morning.last.time, assn.day
    )

    night = create_time_entries(day.last.value, day.last.time, assn.night)

    combined = TimeEntryList(
        early_morning.values + day.values + night.values
    ).unique_and_sorted

    assert combined[0].time == DAY_START_TIME
    assert combined[-1].time == DAY_END_TIME

    # TODO: chek that the length og the range is the same..

    base_time_entries = [i.base_time_entry for i in combined]

    return base_time_entries


def sum_entries(entries: list[BaseTimeEntry]):
    return sum([i.value for i in entries])


def create_venting_year(
    seed: int = SEED,
    operation_start: Date = Date(5, 1),
    operation_end: Date = Date(8, 1),
):
    default_day = create_day_from_single_value(VentingState.CLOSE.value)

    operating_range = xr.date_range(
        create_datetime(DAY_START_TIME, operation_start.python_date),
        create_datetime(DAY_END_TIME, operation_end.python_date),
        freq="D",
    )
    operating_entries: list[DayEntry] = []
    start_value = VentingState.CLOSE

    np_random_generator = np.random.default_rng(seed)
    res = np_random_generator.normal(1)
    print(res)
    children_rng = np_random_generator.spawn(operating_range.size)

    tracker: list[float] = []
    for ix, (curr_date, generator) in enumerate(
        zip(operating_range.date, children_rng)  # pyright: ignore[reportAttributeAccessIssue]
    ):
        entries = create_day_entries(start_value, generator)
        day = create_day_from_time_entries(entries)
        operating_entries.append(DayEntry(Date.from_date(curr_date), day))
        start_value = VentingState(entries[-1].value)

        tracker.append(sum_entries(entries))

    year = create_year_from_day_entries_and_defaults(operating_entries, default_day)

    txarr = xr.DataArray(data=tracker, coords={"datetime": operating_range})

    print(f"{txarr.mean().values=}, {txarr.std().values=}")

    # print(year)
    # plot_year(year, operation_start, Date(5, 2))
    return year
