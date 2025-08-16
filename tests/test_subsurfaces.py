# TODO should all examples live in one directory or with their creators?
from geomeppy.idf import new_idf

from replan2eplus.examples.minimal import get_minimal_case_with_rooms, test_rooms
from replan2eplus.ezobjects.idf import SubsurfaceObject
from replan2eplus.geometry.directions import WallNormal
from replan2eplus.geometry.domain_create import Dimension
from replan2eplus.subsurfaces.interfaces import (
    Location,
    ZoneDirectionEdge,
    ZoneEdge,
    Details,
)
from replan2eplus.subsurfaces.logic import (
    get_surface_between_zone_and_direction,
    get_surface_between_zones,
)
from replan2eplus.subsurfaces.presentation import (
    create_subsurface_for_exterior_edge,
    create_subsurface_for_interior_edge,
)
import pytest

room1, room2 = test_rooms
zone_edge = ZoneEdge(room1.name, room2.name)
zone_drn_edge = ZoneDirectionEdge(
    room1.name, WallNormal.EAST
)  # TODO: WEST should be outer, geometry is messed up

location = Location("mm", "SOUTH_WEST", "SOUTH_WEST")
factor = 4
dimension = Dimension(
    room1.domain.horz_range.size / factor, room1.domain.vert_range.size / factor
)
door_details = Details(dimension, location, "Door")
window_details = Details(dimension, location, "Window")


val = 0.5
ss_obj = SubsurfaceObject("Test", "FakeSurface", val, val, val, val)

# TODO test fail on bad edge..
# @pytest.mark.skip("Not implemented")
# def test_create_edge_with_bad_name():
#     node_a = Node("fake_room", "Zone")
#     with pytest.raises:
#         ...


def test_find_correct_surface_between_zones(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    surf, nb = get_surface_between_zones(zone_edge, case.zones)
    assert surf.surface_name == "Block `room1` Storey 0 Wall 0001_1"
    assert nb == "Block `room2` Storey 0 Wall 0003_1"


def test_find_correct_surface_between_zone_and_direction(
    get_pytest_minimal_case_with_rooms,
):
    case = get_pytest_minimal_case_with_rooms
    surf = get_surface_between_zone_and_direction(zone_drn_edge, case.zones)
    assert (
        surf.surface_name == "Block `room1` Storey 0 Wall 0003"
    )  # TODO just guessing might be wrong
    assert not surf.neighbor


def test_create_subsurface_interior(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurface, partner_suburface = create_subsurface_for_interior_edge(
        zone_edge, door_details, case.zones, case.idf
    )
    assert room1.name in subsurface.name
    assert room2.name in partner_suburface.name


@pytest.mark.skip()
def test_create_subsurface_exterior(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    surface = create_suburface(zone_drn_edge, dimension, location, "Window")


def test_adding_surface_to_random_idf():
    idf = new_idf("test")
    o = idf.newidfobject("WINDOW", **ss_obj._asdict())
    assert o.Name == ss_obj.Name


def test_adding_subsurface_to_ez_idf(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    result = case.idf.add_subsurface("Window", ss_obj)
    assert result.Name == ss_obj.Name

    # Geomeppy IDF doesnt check for valididty, but this method should..


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    obj = SubsurfaceObject("Test", "FakeSurface", 0.5, 0.5, 0.5, 0.5)
    o = case.idf.idf.newidfobject("WINDOW", **obj._asdict())
    o.update(obj._asdict())
    pass
