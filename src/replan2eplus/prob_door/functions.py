from datetime import datetime, time, timedelta

import xarray as xr

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
from replan2eplus.prob_door.interfaces import (
    DEFAULT_FAKE_DATE,
    LEN_INTERVAL,
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


def create_day_entries(start_value: VentingState, seed: int):
    assn = SingleDayVentingAssignment(seed)
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

    assert combined[0].time == time(0, 0)
    assert combined[-1].time == time(23, 59)

    base_time_entries = [i.base_time_entry for i in combined]

    # print(sum([i.value for i in base_time_entries]))
    return base_time_entries


def create_venting_year(
    operation_start: Date = Date(5, 1), operation_end: Date = Date(8, 1)
):
    default_day = create_day_from_single_value(VentingState.CLOSE.value)

    operating_range = xr.date_range(
        create_datetime(DAY_START_TIME, operation_start.python_date),
        create_datetime(DAY_END_TIME, operation_end.python_date),
        freq="D",
    )
    operating_entries: list[DayEntry] = []
    start_value = VentingState.CLOSE

    for ix, i in enumerate(operating_range.date):  # pyright: ignore[reportAttributeAccessIssue]
        entries = create_day_entries(start_value, seed=ix)
        day = create_day_from_time_entries(entries)
        operating_entries.append(DayEntry(Date.from_date(i), day))
        start_value = VentingState(entries[-1].value)

    year = create_year_from_day_entries_and_defaults(operating_entries, default_day)

    # print(year)
    # plot_year(year, operation_start, Date(5, 2))
    return year
