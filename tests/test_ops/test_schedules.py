from datetime import time
from rich import print
from replan2eplus.ops.schedules.interfaces.constants import YEAR_START_DATE
from replan2eplus.ops.schedules.interfaces.day import (
    DAY_END_TIME,
    DAY_START_TIME,
    TimeEntry,
    create_day_from_single_value,
    initialize_array,
    update_arr,
    create_day_from_time_entries,
)
from replan2eplus.ops.schedules.interfaces.year import (
    DayEntry,
    create_year_from_day_entries,
    create_year_from_day_entries_and_defaults,
    initialize_year_array,
    Date,
    update_year_arr,
)
import matplotlib.pyplot as plt


# TODO put into a class as well?
def create_expected_day():
    arr = initialize_array(DAY_START_TIME, DAY_END_TIME)
    t1, t2, t3, t4 = [DAY_START_TIME, time(6, 0), time(9, 15), time(23, 59)]
    v1, v2, v3 = [0, 1, 0]
    arr = update_arr(arr, t1, t2, v1)
    arr = update_arr(arr, t2, t3, v2)
    arr = update_arr(arr, t3, t4, v3)
    return arr


def test_create_day():
    time_entries = [
        TimeEntry(time(6), 0),
        TimeEntry(time(9, 15), 1),
        TimeEntry(time(23, 59), 0),
    ]
    res = create_day_from_time_entries(time_entries)
    exp = create_expected_day()
    assert (res.arr == exp).all()
    # return res


def test_create_day_from_single_value():
    value = 100
    res = create_day_from_single_value(value)
    assert (res.arr == value).all()


zero = -1


class TestYear:
    dates = [
        Date.from_date(YEAR_START_DATE),
        Date(7, 3),
        Date(7, 4),
        Date(7, 5),
        Date(12, 31),
    ]

    basic_day = create_day_from_single_value(0)
    v1 = create_day_from_time_entries(
        [
            TimeEntry(time(7), zero),
            TimeEntry(time(23, 59), 1),
        ]
    )
    v2 = create_day_from_time_entries(
        [
            TimeEntry(time(8), 1),
            TimeEntry(time(23, 59), zero),
        ]
    )

    def create_expected_year(self):
        arr = initialize_year_array()
        dstart, d1, d2, d3, dend = self.dates
        arr = update_year_arr(arr, dstart, d1, self.basic_day)
        arr = update_year_arr(arr, d1, d2, self.v1)
        arr = update_year_arr(arr, d2, d3, self.v2)
        arr = update_year_arr(arr, d3, dend, self.basic_day)
        return arr

    def test_create_year(self):
        d1, d2, d3, d4, d5 = self.dates
        day_entries = [
            DayEntry(d2, self.basic_day),
            DayEntry(d3, self.v1),
            DayEntry(d4, self.v2),
            DayEntry(d5, self.basic_day),
        ]
        res = create_year_from_day_entries(day_entries)
        exp = self.create_expected_year()
        # print(f"{res=}")
        # print(f"{exp=}")
        assert (res.arr == exp).all()

    def test_create_year_with_defaults(self):
        dstart, d1, d2, d3, dend = self.dates
        day_entries = [
            # DayEntry(d2, self.v1),
            DayEntry(d1, self.v1),
            DayEntry(d2, self.v2),
        ]
        res = create_year_from_day_entries_and_defaults(day_entries, self.basic_day)
        exp = self.create_expected_year()
        fig, (ax1, ax2) = plt.subplots(figsize=(12, 8), ncols=2)
        slice_ = slice(d1.minus_one.python_date, d2.plus_one.python_date)
        res.arr.sel(datetime=slice_).plot.line(ax=ax1)
        exp.sel(datetime=slice_).plot.line(ax=ax2)
        plt.show()

        # print(f"{res=}")
        # print(f"{exp=}")
        assert (res.arr == exp).all()


if __name__ == "__main__":
    ty = TestYear()
    ty.test_create_year_with_defaults()
    # print(ty.create_expected_year())
    # res = initialize_year_array()
    # print(res)
