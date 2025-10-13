import pytest

from replan2eplus.examples.cases.minimal import get_minimal_case_with_rooms
from replan2eplus.examples.subsurfaces import (
    SubsurfaceInputExample,
    room1,
    room2,
)
from replan2eplus.ezobjects.subsurface import Edge
from replan2eplus.geometry.directions import WallNormalLiteral
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.plane import Plane
from replan2eplus.geometry.range import Range
from replan2eplus.ops.subsurfaces.interfaces import (
    Detail,
    Dimension,
    Location,
    SubsurfaceInputs2,
    EdgeGroup,
)
from replan2eplus.ops.subsurfaces.presentation import create_subsurfaces

# TODO clean up + test throwing error if the dimensions are too large..
dimension = Dimension(width=1 / 3, height=1)
mm_nw = Location("mm", "NORTH_WEST", "NORTH_WEST")

x_edge_detail_groups: list[tuple[WallNormalLiteral, float]] = [
    ("SOUTH", 0),
    ("NORTH", 1),
]


# @pytest.mark.skip()
@pytest.mark.parametrize("direction, plane_loc", x_edge_detail_groups)
def test_subsurface_x_plane(get_pytest_minimal_case_with_rooms, direction, plane_loc):
    edge = Edge(room2.name, direction)
    detail = Detail(dimension, mm_nw, "Window")
    domain = Domain(
        Range(1 + dimension.width, 1 + (2 * dimension.width)),
        Range(1, 2),
        Plane("Y", plane_loc),
    )
    case = get_pytest_minimal_case_with_rooms
    input = SubsurfaceInputs2([EdgeGroup([edge], detail, "Zone_Direction")])
    subsurface = create_subsurfaces(input, case.zones, case.idf)[0]
    assert subsurface.domain == domain


y_edge_detail_groups: list[tuple[Edge, float]] = [
    (Edge(room1.name, "WEST"), 0),
    (Edge(room2.name, "EAST"), 2),
]



@pytest.mark.parametrize("edge, plane_loc", y_edge_detail_groups)
def test_subsurface_y_plane(get_pytest_minimal_case_with_rooms, edge, plane_loc):
    detail = Detail(dimension, mm_nw, "Window")
    domain = Domain(
        Range(dimension.width, (2 * dimension.width)),
        Range(1, 2),
        Plane("X", plane_loc),
    )
    case = get_pytest_minimal_case_with_rooms

    input = SubsurfaceInputs2([EdgeGroup([edge], detail, "Zone_Direction")])
    subsurface = create_subsurfaces(input, case.zones, case.idf)[0]
    assert subsurface.domain == domain


def test_subsurface_equality(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    eq_subsurfaces = [i for i in case.subsurfaces if i.edge.space_b == room2.name]
    assert len(eq_subsurfaces) == 2
    ss1, ss2 = eq_subsurfaces
    assert ss1 == ss2


if __name__ == "__main__":
    pass
    # case = get_minimal_case_with_rooms()
    # edge, detail, domain = (
    #     Edge(room2.name, "EAST"),
    #     Detail(dimension, mm_nw, "Window"),
    #     Domain(
    #         Range(1 + dimension.width, 1 + (2 * dimension.width)),
    #         Range(1, 2),
    #         Plane("X", 2),
    #     ),
    # )
    # input = SubsurfaceInputExample(edges=[edge], details=[detail], map_={0: [0]}).inputs
    # subsurface = create_subsurfaces(input, case.zones, case.idf)[0]
    # print(subsurface.domain)
    # print(subsurface)


# TODO! stronger checks on tehse? rn just checking that get the right number of subsurfaces.. are they on the right faces?
