import pytest
from replan2eplus.examples.cases.minimal import get_minimal_case
from eppy.modeleditor import IDF
from replan2eplus.paths import PATH_TO_WEATHER_FILE, THROWAWAY_PATH
from replan2eplus.examples.paths import PATH_TO_IDD, PATH_TO_MINIMAL_IDF
from replan2eplus.examples.mat_and_const import get_minimal_case_with_materials
from replan2eplus.ops.schedule.interfaces import Day, TimeEntry, HOURS_PER_DAY
import numpy as np
from rich import print


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
    assert (day.create_array() == expected_arr).all()


def test_single_value_day_entry():
    day = Day.from_single_value(10)
    expected_arr = np.full(shape=(HOURS_PER_DAY), fill_value=10)
    arr = day.create_array()
    assert (arr == expected_arr).all()


@pytest.mark.skip()
def test_add_sched(case):
    idf = case.idf.idf  # this is a pointer to the cases idf...
    data = {
        "Name": "Test",
        "Schedule_Type_Limits_Name": "Fraction",
        "Field_1": "12/31",
        "Field_2": "AllDays",
        "Field_3": "7:00",
        "Field_4": 1,
        "Field_5": "17:00",
        "Field_6": 0,
        "Field_8": "24:00",
        "Field_9": 1,
    }
    o = idf.newidfobject("SCHEDULE:COMPACT", **data)
    print(o)
    return case


@pytest.mark.skip()
def test_minimal_work_case():
    case = get_minimal_case_with_materials()
    case = test_add_sched(case)
    case.save_and_run_case(path_=THROWAWAY_PATH)


if __name__ == "__main__":
    test_single_value_day_entry()
