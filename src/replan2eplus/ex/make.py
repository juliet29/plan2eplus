from replan2eplus.ex.rooms import Rooms
from replan2eplus.ex.subsurfaces import details
from replan2eplus.ezcase.ez import EZ
from replan2eplus.ops.subsurfaces.interfaces import Edge
from replan2eplus.ops.subsurfaces.user_interfaces import EdgeGroup, SubsurfaceInputs
from replan2eplus.paths import DynamicPaths, ep_paths
from replan2eplus.visuals.base.base_plot import BasePlot
from pathlib import Path

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


def make_data_plot():
    #
    pass
