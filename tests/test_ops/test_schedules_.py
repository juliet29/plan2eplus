# import pytest
# from replan2eplus.ops.schedules.interfaces import (
#     Day,
#     TimeEntry,
#     HOURS_PER_DAY,
#     DayEntry,
#     Year,
# )
# import numpy as np
# # from replan2eplus.ops.schedules.idfobject import ScheduleFileObject, ScheduleTypeLimits


# test_days: list[tuple[list[TimeEntry], np.ndarray]] = [
#     ([TimeEntry(12, 1), TimeEntry(24, 0)], np.concat([np.ones(12), np.zeros(12)])),
#     (
#         [TimeEntry(6, 1), TimeEntry(12, 0), TimeEntry(24, 1)],
#         np.concat([np.ones(6), np.zeros(6), np.ones(12)]),
#     ),
# ]


# @pytest.mark.skip
# @pytest.mark.parametrize("times, expected_arr", test_days)
# def test_day_entry(times, expected_arr):
#     day = Day(times)
#     assert (day.array == expected_arr).all()


# @pytest.mark.skip
# def test_single_value_day_entry():
#     day = Day.from_single_value(10)
#     expected_arr = np.full(shape=(HOURS_PER_DAY), fill_value=10)
#     arr = day.array
#     assert (arr == expected_arr).all()


# @pytest.mark.skip
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

#     # def test_file_write(self):
#     #     self.year.write_to_file()


# # @pytest.mark.skip()
# @pytest.mark.skip
# def add_test_sched(case: EZCase):
#     idf = case.idf.idf
#     lims = ScheduleTypeLimits("Test", -1, 40, "Discrete", "Dimensionless")
#     o = idf.newidfobject(lims.key, **lims.values)
#     test_year = TestYear()
#     file_obj = ScheduleFileObject("TestSched", "Test", test_year.test_path)
#     o2 = idf.newidfobject(file_obj.key, **file_obj.values)
#     # print(o)
#     # print(o2)

#     return case


# # @pytest.mark.skip()
# @pytest.mark.skip
# def test_minimal_work_case():
#     case = get_minimal_case_with_materials()
#     case = add_test_sched(case)
#     case.save_and_run_case(path_=THROWAWAY_PATH)
#     assert 1


# if __name__ == "__main__":
#     # case = get_minimal_case_with_materials()
#     test_minimal_work_case()
#     # idf = case.idf.idf
#     # idf.to_obj()
#     # test_add_sched(case)
#     # t = TestYear
#     # t.year.write_to_file(static_paths.temp / "sample_schedule.csv")
