from replan2eplus.ops.schedules.interfaces.day import Day, TimeEntry
from rich import print
import pytest
import numpy as np

from replan2eplus.ops.schedules.interfaces.constants import HOURS_PER_DAY
from replan2eplus.ops.schedules.interfaces.year import DayEntry


def test_create_day():
    time_entries = [TimeEntry(6, 0), TimeEntry(9, 1), TimeEntry(24, 0)]
    day = Day(time_entries)
    print(day.array)


def test_create_day_from_single_value():
    day = Day.from_single_value(1)
    print(day.array)


test_days: list[tuple[list[TimeEntry], np.ndarray]] = [
    ([TimeEntry(12, 1), TimeEntry(24, 0)], np.concat([np.ones(12), np.zeros(12)])),
    (
        [TimeEntry(6, 1), TimeEntry(12, 0), TimeEntry(24, 1)],
        np.concat([np.ones(6), np.zeros(6), np.ones(12)]),
    ),
]


@pytest.mark.parametrize("times, expected_arr", test_days)
def test_day_entry(times, expected_arr):
    day = Day(times)
    assert (day.array == expected_arr).all()


def test_single_value_day_entry():
    day = Day.from_single_value(10)
    expected_arr = np.full(shape=(HOURS_PER_DAY), fill_value=10)
    arr = day.array
    assert (arr == expected_arr).all()


# class TestYear:
#     default_day = Day.from_single_value(0)
#     special_day = Day.from_single_value(10)
#     day_entries = [DayEntry(1, 1, special_day)]

#     year = Year(default_day, day_entries)
#     test_path = static_paths.temp / "sample_schedule.csv"

#     def test_year_entry(self):
#         assert (
#             self.year.array[0:24] == np.full(shape=(HOURS_PER_DAY), fill_value=10)
#         ).all()
#         assert (
#             self.year.array[24:48] == np.full(shape=(HOURS_PER_DAY), fill_value=0)
#         ).all()


if __name__ == "__main__":
    test_create_day()
    test_create_day_from_single_value()
