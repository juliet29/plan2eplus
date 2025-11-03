from datetime import time
from rich import print
from replan2eplus.ops.schedules.interfaces.constants import START_DATE
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
    initialize_year_array,
    Date,
    update_year_arr,
)


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


class TestYear:
    dates = [
        Date.from_date(START_DATE),
        Date(7, 2),
        Date(7, 3),
        Date(7, 4),
        Date(12, 31),
    ]
    basic_day = create_day_from_single_value(100)
    v1 = create_day_from_time_entries(
        [
            TimeEntry(time(7), 0),
            TimeEntry(time(23, 59), 1),
        ]
    )
    v2 = create_day_from_time_entries(
        [
            TimeEntry(time(8), 1),
            TimeEntry(time(23, 59), 0),
        ]
    )

    def create_expected_year(self):
        arr = initialize_year_array()
        d1, d2, d3, d4, d5 = self.dates
        arr = update_year_arr(arr, d1, d2, self.basic_day)
        arr = update_year_arr(arr, d2, d3, self.v1)
        arr = update_year_arr(arr, d3, d4, self.v2)
        arr = update_year_arr(arr, d4, d5, self.basic_day)
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
    ty = TestYear()
    ty.test_create_year()
    # print(ty.create_expected_year())
    # res = initialize_year_array()
    # print(res)
