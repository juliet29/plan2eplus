from datetime import date, time, timedelta, datetime
import pytest
from html import entities
from rich import print
import test
from replan2eplus.prob_door.interfaces import (
    DefaultDistributions,
    Distributions,
    GeometricDisribution,
    VentingState,
    create_time_entries,
    create_day_entries,
    is_crossing_midnight,
)


def test_datetime_addition():
    simple_date = date(2025, 1, 1)
    simple_time = time(1, 0)
    td = 3 * timedelta(minutes=15)
    simple_datetime = datetime.combine(simple_date, simple_time)
    new_datetime = simple_datetime + td
    new_time = new_datetime.time()
    assert new_time == time(1, 45)


def test_sampling_geom_dist():
    X = GeometricDisribution(0.3)
    res = X.sample()
    assert type(res) is int


def show_geom_dist():
    X = GeometricDisribution(0.99)
    X.probability_mass_function
    # X.stats
    X.show_summary()


def test_create_time_entries():
    start_value = VentingState.CLOSE
    start_time = time(18, 0)
    end_time = time(23, 59)
    dist = DefaultDistributions.night
    entries = create_time_entries(start_value, start_time, end_time, dist)
    assert len(entries.values) > 2
    assert entries.values[1].value == VentingState.OPEN
    print(entries)


time_test: list[tuple[time, time, bool]] = [
    (time(23, 37), time(0, 53), True),
    (time(23, 37), time(23, 53), False),
]


@pytest.mark.parametrize("tprev, tnext, exp", time_test)
def test_is_crossing_midnight(tprev, tnext, exp):
    res = is_crossing_midnight(tprev, tnext)
    assert res == exp


if __name__ == "__main__":
    create_day_entries()
    #test_create_time_entries()
    # show_geom_dist()
