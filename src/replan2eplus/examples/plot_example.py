from replan2eplus.examples.defaults import PATH_TO_IDD
from replan2eplus.ezcase.read import ExistCase
from replan2eplus.paths import TWO_ROOM_AIRBOUNDARY_RESULTS
from replan2eplus.results.sql import get_qoi
from replan2eplus.visuals.data_plot import DataPlot


from pathlib import Path


def plot_zones_and_connections(
    path_to_idd: Path = PATH_TO_IDD,
    path: Path = TWO_ROOM_AIRBOUNDARY_RESULTS,
    hour: int = 1,
):
    case = ExistCase(path_to_idd, path / "out.idf")

    pressure = get_qoi("AFN Node Total Pressure", path)
    data_at_noon = pressure.select_time(hour)

    flow_12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate", path)
    flow_21 = get_qoi("AFN Linkage Node 2 to Node 1 Volume Flow Rate", path)
    combined_flow = flow_12.select_time(hour) - flow_21.select_time(hour)

    dp = DataPlot(case.zones)
    dp.plot_zones_with_data(data_at_noon)
    dp.plot_zone_names()
    dp.plot_cardinal_names()
    dp.plot_subsurfaces_and_surfaces(case.afn, case.airboundaries, case.subsurfaces)
    dp.plot_connections_with_data(combined_flow, case.subsurfaces, case.airboundaries)

    return dp
