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


def plot_zone_data():
    case = ExistCase(PATH_TO_IDD, TWO_ROOM_RESULTS / "out.idf")
    pressure = get_qoi("AFN Node Total Pressure")
    data_at_noon = pressure.select_time(12)

    dp = DataPlot(case.zones)
    dp.plot_zones_with_data(data_at_noon)
    dp.plot_zone_names()
    dp.plot_cardinal_names()

    # TODO set up airboundary read on exist case..
    # dp.plot_subsurfaces_and_surfaces()
    return dp


def plot_connection_data():
    case = ExistCase(PATH_TO_IDD, TWO_ROOM_RESULTS / "out.idf")
    flow_12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate")
    flow_21 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate")
    combined_flow = flow_12.select_time(1) + flow_21.select_time(1)

    print(combined_flow)
    print(combined_flow.space_names)
    dp = DataPlot(case.zones)
    dp.plot_zones()
    dp.plot_zone_names()
    dp.plot_cardinal_names()
    dp.plot_connections_with_data(combined_flow, case.subsurfaces)

    # data_at_noon = pressure.select_time(12)

    # case.initialize_idf()
    # case.get_objects()
    # dp = DataPlot(case.zones)
    # dp.plot_zones_with_data(data_at_noon)
    # dp.plot_zone_names()
    # dp.plot_cardinal_names()
    return dp 


def test_space_names():
    case = ExistCase(PATH_TO_IDD, TWO_ROOM_RESULTS / "out.idf")
    pressure = get_qoi("AFN Node Total Pressure")
    data_at_noon = pressure.select_time(12)
    res = filter_data_arr(data_at_noon, [i.zone_name.upper() for i in case.zones])
    assert res.shape == (1, 1)
    return


def test_plot_zones():
    plot_zone_data()
    assert 1


if __name__ == "__main__":
    dp = plot_connection_data()
    dp.show()
