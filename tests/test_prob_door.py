from datetime import date, time, timedelta, datetime
import pytest
from rich import print
from replan2eplus.prob_door.functions import (
    create_time_entries,
    create_venting_year,
    is_crossing_midnight,
)
from replan2eplus.prob_door.interfaces import (
    GeometricDisribution,
    SingleDayVentingAssignment,
    VentingState,
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
    assn = SingleDayVentingAssignment(seed=0)
    entries = create_time_entries(start_value, start_time, assn.night)
    assert len(entries.values) > 2
    assert entries.values[1].value == VentingState.OPEN
    print(entries)


midnight_test: list[tuple[time, time, bool]] = [
    (time(23, 37), time(0, 53), True),
    (time(23, 37), time(23, 53), False),
]


@pytest.mark.parametrize("tprev, tnext, exp", midnight_test)
def test_is_crossing_midnight(tprev, tnext, exp):
    res = is_crossing_midnight(tprev, tnext)
    assert res == exp


def test_create_venting_year():
    year = create_venting_year()
    assert 1


if __name__ == "__main__":
    create_venting_year()

    # test_create_time_entries()
    # show_geom_dist()
