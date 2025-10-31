from replan2eplus.ex.rooms import Rooms
from replan2eplus.ex.subsurfaces import details
from replan2eplus.ezcase.ez import EZ, ep_paths
from replan2eplus.ops.subsurfaces.interfaces import Edge
from replan2eplus.ops.subsurfaces.user_interfaces import EdgeGroup, SubsurfaceInputs
from replan2eplus.paths import DynamicPaths, ep_paths
from replan2eplus.results.sql import get_qoi
from replan2eplus.visuals.base.base_plot import BasePlot
from pathlib import Path

from replan2eplus.visuals.data.data_plot import DataPlot

r1, r2 = Rooms().two_room_list
airboundary_edges = [Edge(r1.name, r2.name)]


def make_test_case(
    edge_groups: list[EdgeGroup],
    airboundary_edges: list[Edge] = [],
    output_path: Path | None = None,
    afn: bool = False,
    rooms=Rooms().two_room_list,
):
    case = (
        EZ()
        .add_zones(rooms)
        .add_subsurfaces(SubsurfaceInputs(edge_groups, details), airboundary_edges)
        .add_constructions()
    )
    if afn:
        case.add_airflow_network()
    if output_path:
        case.output_path = output_path
    else:
        case.output_path = DynamicPaths.THROWAWAY_PATH
    case.epw_path = ep_paths.default_weather

    return case


def make_base_plot(case: EZ):
    bp = (
        BasePlot(case.objects.zones, cardinal_expansion_factor=1.8)
        .plot_zones()
        .plot_zone_names()
        .plot_cardinal_names()
        .plot_subsurfaces_and_surfaces(
            case.objects.airflow_network,
            case.objects.airboundaries,
            case.objects.subsurfaces,
        )
        .plot_connections(
            case.objects.airflow_network,
            case.objects.airboundaries,
            case.objects.subsurfaces,
        )
        # uniqueness matters if want to label the windows and doors, but think the legend takes care of this?
    )

    return bp


def make_data_plot(
    path: Path,
    hour: int = 12,
):
    case = EZ(idf_path=path / ep_paths.idf_name)

    pressure = get_qoi("AFN Node Total Pressure", path)
    data_at_noon = pressure.select_time(hour)
    # print(data_at_noon)

    flow_12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate", path)
    flow_21 = get_qoi("AFN Linkage Node 2 to Node 1 Volume Flow Rate", path)
    combined_flow = flow_12.select_time(hour) - flow_21.select_time(hour)
    # print(combined_flow)

    dp = DataPlot(case.objects.zones)
    dp.plot_zones_with_data(data_at_noon)
    dp.plot_zone_names()
    dp.plot_cardinal_names()
    dp.plot_subsurfaces_and_surfaces(
        case.objects.airflow_network,
        case.objects.airboundaries,
        case.objects.subsurfaces,
    )
    dp.plot_connections_with_data(
        combined_flow, case.objects.subsurfaces, case.objects.airboundaries
    )

    return dp
