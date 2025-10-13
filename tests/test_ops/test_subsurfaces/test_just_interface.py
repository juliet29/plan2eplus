from replan2eplus.examples.subsurfaces import (
    subsurface_inputs_dict, details, e0
)
from replan2eplus.ops.subsurfaces.interfaces import EdgeGroup, SubsurfaceInputs2
import pytest

from replan2eplus.ops.subsurfaces.logic.prepare import create_ss_name
from replan2eplus.ops.subsurfaces.presentation import create_subsurfaces


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


def test_simple_subsurface_desc(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    input = SubsurfaceInputs2(
        [EdgeGroup.from_tuple_edges([e0], details["door"], "Zone_Zone")]
    )
    subsurfaces = create_subsurfaces(input, case.zones, case.idf)
    assert len(subsurfaces) == 2


def test_creating_subsurfaces_simple(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurfaces = create_subsurfaces(
        subsurface_inputs_dict["simple"], case.zones, case.idf
    )
    assert len(subsurfaces) == 3


def test_creating_subsurfaces_three_details(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurfaces = create_subsurfaces(
        subsurface_inputs_dict["three_details"], case.zones, case.idf
    )
    assert len(subsurfaces) == 5


def test_creating_interior_subsurface(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurfaces = create_subsurfaces(
        subsurface_inputs_dict["interior"], case.zones, case.idf
    )
    assert len(subsurfaces) == 2
    ss1 = subsurfaces[0]
    ss2 = subsurfaces[1]
    assert ss1._epbunch.Outside_Boundary_Condition_Object == create_ss_name(
        ss2.surface.surface_name, details["door"])
