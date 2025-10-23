from replan2eplus.ex.subsurfaces import details, e0
from replan2eplus.ops.subsurfaces.idfobject import IDFSubsurface
from replan2eplus.ops.subsurfaces.logic.prepare import create_ss_name
from replan2eplus.ops.subsurfaces.user_interfaces import EdgeGroup, SubsurfaceInputs
import pytest
from replan2eplus.ex.main import Cases, Interfaces
from replan2eplus.ops.subsurfaces.presentation import create_subsurfaces
from replan2eplus.ops.zones.idfobject import IDFZone
from replan2eplus.ops.surfaces.idfobject import IDFSurface
from rich import print


def test_init_edge_group():
    edges = [("a", "NORTH"), ("b", "SOUTH")]
    eg = EdgeGroup.from_tuple_edges(edges, "", "Zone_Direction")
    assert eg


def test_init_edge_group_zones():
    edges = [("a", "0"), ("b", "1")]
    eg = EdgeGroup.from_tuple_edges(edges, "", "Zone_Zone")
    assert eg


def test_bad_init_edge_group():
    edges = [("a", "0"), ("b", "1")]
    with pytest.raises(AssertionError):
        EdgeGroup.from_tuple_edges(edges, "", "Zone_Direction")


# TODO combine with just interface..


def test_simple_subsurface_desc():
    case = Cases().two_room
    input = SubsurfaceInputs(
        [EdgeGroup.from_tuple_edges([e0], details["door"], "Zone_Zone")]
    )
    subsurfaces = create_subsurfaces(
        input, case.objects.surfaces, case.objects.zones, case.idf
    )
    print(subsurfaces)
    assert len(subsurfaces) == 2


def test_creating_subsurfaces_simple():
    case = Cases().two_room
    subsurfaces = create_subsurfaces(
        Interfaces.subsurfaces.simple,
        case.objects.surfaces,
        case.objects.zones,
        case.idf,
    )
    assert len(subsurfaces) == 3


def test_creating_subsurfaces_three_details():
    case = Cases().two_room
    subsurfaces = create_subsurfaces(
        Interfaces.subsurfaces.three_details,
        case.objects.surfaces,
        case.objects.zones,
        case.idf,
    )
    assert len(subsurfaces) == 5


def test_creating_interior_subsurface():
    case = Cases().two_room
    subsurfaces = create_subsurfaces(
        Interfaces.subsurfaces.interior,
        case.objects.surfaces,
        case.objects.zones,
        case.idf,
    )
    assert len(subsurfaces) == 2
    ss1 = subsurfaces[0]
    ss2 = subsurfaces[1]
    assert ss2.surface.neighbor_name
    assert ss1.subsurface_name == create_ss_name(
        ss2.surface.neighbor_name, details["door"]
    )


# def test_creating_subsurfaces_three_details(get_pytest_minimal_case_with_rooms):
#     case = get_pytest_minimal_case_with_rooms
#     subsurfaces = create_subsurfaces(
#         subsurface_inputs_dict["three_details"], case.zones, case.idf
#     )
#     assert len(subsurfaces) == 5


# def test_creating_interior_subsurface(get_pytest_minimal_case_with_rooms):
#     case = get_pytest_minimal_case_with_rooms
#     subsurfaces = create_subsurfaces(
#         subsurface_inputs_dict["interior"], case.zones, case.idf
#     )
if __name__ == "__main__":
    # case = Cases().example
    # subsurfaces = IDFSubsurface.read(case.idf)
    # print(subsurfaces[0])
    test_simple_subsurface_desc()
