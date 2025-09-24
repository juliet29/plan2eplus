from replan2eplus.paths import TWO_ROOM_RESULTS
from replan2eplus.ezcase.read import ExistCase
from replan2eplus.examples.defaults import PATH_TO_IDD
from replan2eplus.results.collections import (
    DFC,
    QOIResult,
    sqlcollections_to_qoi_result,
)
from replan2eplus.results.sql import create_result_for_qoi, get_sql_results
from replan2eplus.idfobjects.variables import OutputVariables
from rich import print as rprint
import pytest
import numpy as np
from replan2eplus.visuals.data_plot import DataForPlot, DataPlot, filter_data_arr


def get_qoi(qoi: OutputVariables):
    sql = get_sql_results(TWO_ROOM_RESULTS)
    return create_result_for_qoi(sql, qoi)


def plot_values():
    case = ExistCase(PATH_TO_IDD, TWO_ROOM_RESULTS / "out.idf")
    pressure = get_qoi("AFN Node Total Pressure")
    data_at_noon = pressure.select_time(12)

    case.initialize_idf()
    case.get_objects()
    dp = DataPlot(case.zones)
    dp.plot_zones_with_data(data_at_noon)
    dp.plot_zone_names()
    dp.plot_cardinal_names()
    return dp 


def test_space_names():
    case = ExistCase(PATH_TO_IDD, TWO_ROOM_RESULTS / "out.idf")
    pressure = get_qoi("AFN Node Total Pressure")
    data_at_noon = pressure.select_time(12)
    res = filter_data_arr(data_at_noon, [i.zone_name.upper() for i in case.zones])
    assert res.shape == (1, 1)
    return

def test_plot_zones():
    plot_values()
    assert 1

if __name__ == "__main__":
    plot_values ()
