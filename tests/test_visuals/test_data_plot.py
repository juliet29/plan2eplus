import pytest
from replan2eplus.examples.paths import PATH_TO_IDD
from replan2eplus.ezcase.read import ExistCase, get_afn_objects
from replan2eplus.idfobjects.variables import OutputVariables
from replan2eplus.paths import TWO_ROOM_RESULTS, TWO_ROOM_AIRBOUNDARY_RESULTS
from replan2eplus.results.sql import create_result_for_qoi, get_sql_results
from replan2eplus.visuals.data.data_plot import DataPlot, filter_data_arr
from pathlib import Path

from replan2eplus.examples.plots.data_plot import plot_zones_and_connections


def get_qoi(qoi: OutputVariables, path: Path = TWO_ROOM_RESULTS):
    sql = get_sql_results(path)
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
    # TODO the sql needs to be linked to the case reading!!!!
    case = ExistCase(PATH_TO_IDD, TWO_ROOM_AIRBOUNDARY_RESULTS / "out.idf")
    flow_12 = get_qoi(
        "AFN Linkage Node 1 to Node 2 Volume Flow Rate", TWO_ROOM_AIRBOUNDARY_RESULTS
    )
    flow_21 = get_qoi(
        "AFN Linkage Node 2 to Node 1 Volume Flow Rate", TWO_ROOM_AIRBOUNDARY_RESULTS
    )
    combined_flow = flow_12.select_time(1) - flow_21.select_time(1)

    print(combined_flow)
    print(combined_flow.space_names)
    dp = DataPlot(case.zones)
    dp.plot_zones()
    dp.plot_zone_names()
    dp.plot_cardinal_names()
    dp.plot_subsurfaces_and_surfaces(
        case.airflownetwork, case.airboundaries, case.subsurfaces
    )
    dp.plot_connections_with_data(combined_flow, case.subsurfaces, case.airboundaries)

    return dp


@pytest.mark.xfail()
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


def test_plot_connections():
    plot_connection_data()
    assert 1


# MOVE ELSEWHERE -> test of existing, ot dataplot..
def test_get_afn_values():
    case = ExistCase(PATH_TO_IDD, TWO_ROOM_AIRBOUNDARY_RESULTS / "out.idf")
    assert len(case.airflownetwork.zones) == 2
    assert len(case.airflownetwork.airboundaries) == 1
    assert len(case.airflownetwork.subsurfaces) == 3


if __name__ == "__main__":
    dp = plot_zones_and_connections(TWO_ROOM_RESULTS)
    dp.show()
    # get_afn_values()
    pass
