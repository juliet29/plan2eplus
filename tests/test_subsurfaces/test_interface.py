from replan2eplus.geometry.directions import WallNormalLiteral, WallNormalNamesList
from replan2eplus.geometry.domain import Domain
from replan2eplus.ops.subsurfaces.interfaces import Dimension
from replan2eplus.geometry.plane import Plane
from replan2eplus.geometry.range import Range
from replan2eplus.ops.subsurfaces.interfaces import Details, Location
from replan2eplus.ops.subsurfaces.logic.prepare import create_ss_name
from replan2eplus.ops.subsurfaces.presentation import create_subsurfaces
from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.examples.subsurfaces import (
    simple_subsurface_inputs,
    three_details_subsurface_inputs,
    interior_subsurface_inputs,
    room2,
    room1,
    SubsurfaceInputExample,
)
from replan2eplus.ezobjects.subsurface import Edge, Subsurface
import pytest


def test_creating_subsurfaces_simple(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurfaces = create_subsurfaces(
        simple_subsurface_inputs.inputs, case.zones, case.idf
    )
    assert len(subsurfaces) == 3


def test_creating_subsurfaces_three_details(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurfaces = create_subsurfaces(
        three_details_subsurface_inputs.inputs, case.zones, case.idf
    )
    assert len(subsurfaces) == 5


def test_creating_interior_subsurface(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurfaces = create_subsurfaces(
        interior_subsurface_inputs.inputs, case.zones, case.idf
    )
    assert len(subsurfaces) == 2
    ss1 = subsurfaces[0]
    ss2 = subsurfaces[1]
    assert ss1._epbunch.Outside_Boundary_Condition_Object == create_ss_name(
        ss2.surface.surface_name, interior_subsurface_inputs.details[0]
    )


def test_subsurface_equality(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    eq_subsurfaces = [i for i in case.subsurfaces if i.edge.space_b == room2.name]
    assert len(eq_subsurfaces) == 2
    ss1, ss2 = eq_subsurfaces
    assert ss1 == ss2


# TODO clean up + test throwing error if the dimensions are too large..
dimension = Dimension(width=1 / 3, height=1)
mm_nw = Location("mm", "NORTH_WEST", "NORTH_WEST")

x_edge_detail_groups: list[tuple[WallNormalLiteral, float]] = [
    ("SOUTH", 0),
    ("NORTH", 1),
]


@pytest.mark.parametrize("direction, plane_loc", x_edge_detail_groups)
def test_subsurface_x_plane(get_pytest_minimal_case_with_rooms, direction, plane_loc):
    edge = Edge(room2.name, direction)
    detail = Details(dimension, mm_nw, "Window")
    domain = Domain(
        Range(1 + dimension.width, 1 + (2 * dimension.width)),
        Range(1, 2),
        Plane("Y", plane_loc),
    )
    case = get_pytest_minimal_case_with_rooms
    input = SubsurfaceInputExample(edges=[edge], details=[detail], map_={0: [0]}).inputs
    subsurface = create_subsurfaces(input, case.zones, case.idf)[0]
    assert subsurface.domain == domain


y_edge_detail_groups: list[tuple[Edge, float]] = [
    (Edge(room1.name, "WEST"), 0),
    (Edge(room2.name, "EAST"), 2),
]


@pytest.mark.parametrize("edge, plane_loc", y_edge_detail_groups)
def test_subsurface_y_plane(get_pytest_minimal_case_with_rooms, edge, plane_loc):
    detail = Details(dimension, mm_nw, "Window")
    domain = Domain(
        Range(dimension.width, (2 * dimension.width)),
        Range(1, 2),
        Plane("X", plane_loc),
    )
    case = get_pytest_minimal_case_with_rooms
    input = SubsurfaceInputExample(edges=[edge], details=[detail], map_={0: [0]}).inputs
    subsurface = create_subsurfaces(input, case.zones, case.idf)[0]
    assert subsurface.domain == domain


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    edge, detail, domain = (
        Edge(room2.name, "EAST"),
        Details(dimension, mm_nw, "Window"),
        Domain(
            Range(1 + dimension.width, 1 + (2 * dimension.width)),
            Range(1, 2),
            Plane("X", 2),
        ),
    )
    input = SubsurfaceInputExample(edges=[edge], details=[detail], map_={0: [0]}).inputs
    subsurface = create_subsurfaces(input, case.zones, case.idf)[0]
    print(subsurface.domain)
    print(subsurface)

# TODO! stronger checks on tehse? rn just checking that get the right number of subsurfaces.. are they on the right faces?
