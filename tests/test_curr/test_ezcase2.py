from rich import print

from replan2eplus.ex.afn import EdgeGroups as AFNEdgeGroups
from replan2eplus.ex.rooms import Rooms
from replan2eplus.ex.subsurfaces import details
from replan2eplus.ezcase.ez import EZ
from replan2eplus.ops.subsurfaces.interfaces import Edge
from replan2eplus.ops.subsurfaces.user_interfaces import EdgeGroup, SubsurfaceInputs
from replan2eplus.paths import THROWAWAY_PATH, ep_paths

r1, r2 = Rooms().two_room_list
airboundary_edges = [Edge(r1.name, r2.name)]


def make_test_case(
    edge_groups: list[EdgeGroup],
    airboundary_edges: list[Edge] = [],
    afn: bool = False,
    rooms=[r1, r2],
):
    case = (
        EZ()
        .add_zones(rooms)
        .add_subsurfaces(SubsurfaceInputs(edge_groups, details), airboundary_edges)
        .add_constructions()
    )
    if afn:
        case.add_airflow_network()
    case.output_path = THROWAWAY_PATH
    case.epw_path = ep_paths.default_weather

    return case


def test_case_basic():
    case = make_test_case(AFNEdgeGroups.A_ew)
    case.save_and_run(run=True)
    assert 1


def test_case_airboudary():
    case = make_test_case(AFNEdgeGroups.A_ns, airboundary_edges)
    case.save_and_run(run=True)
    assert 1


def test_case_airboundary_afn():
    case = make_test_case(AFNEdgeGroups.A_ns, airboundary_edges, afn=True)
    case.save_and_run(run=True)
    assert 1


# ortho domains..
# running from an existing idf -> to run don't need to read an idf really, that is just needed for graphing.. so maybe reading existing objects is a flag that can get turned on or off.. if adding new things, should read ..


if __name__ == "__main__":
    case = make_test_case(AFNEdgeGroups.A_ns, [Edge(r1.name, r2.name)], afn=True)
    case.save_and_run(run=True)
