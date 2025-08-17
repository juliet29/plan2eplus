from geomeppy.idf import new_idf

from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.examples.subsurfaces import (
    zone_edge,
    zone_drn_edge,
    window_details,
    door_details,
    room1,
    room2,
    subsurface_object,
)
from replan2eplus.geometry.directions import WallNormal
from replan2eplus.subsurfaces.interfaces import (
    Edge,
    flatten_dict_map,
)
from replan2eplus.subsurfaces.logic import (
    get_surface_between_zone_and_direction,
    get_surface_between_zones,
)
from replan2eplus.subsurfaces.presentation import (
    create_subsurface_for_exterior_edge,
    create_subsurface_for_interior_edge,
)


# TODO test fail on bad edge..
# @pytest.mark.skip("Not implemented")
# def test_create_edge_with_bad_name():
#     node_a = Node("fake_room", "Zone")
#     with pytest.raises:
#         ...


def test_adding_surface_to_random_idf():
    idf = new_idf("test")
    o = idf.newidfobject("WINDOW", **subsurface_object._asdict())
    assert o.Name == subsurface_object.Name


def test_adding_subsurface_to_ez_idf(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    result = case.idf.add_subsurface("Window", subsurface_object)
    assert result.Name == subsurface_object.Name


def test_find_correct_surface_between_zones(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    surf, nb = get_surface_between_zones(zone_edge, case.zones)
    assert surf.direction == WallNormal.EAST
    assert nb.direction == WallNormal.WEST


def test_find_correct_surface_between_zone_and_direction(
    get_pytest_minimal_case_with_rooms,
):
    case = get_pytest_minimal_case_with_rooms
    surf = get_surface_between_zone_and_direction(zone_drn_edge, case.zones)
    assert (
        surf.direction == WallNormal.WEST
    )  # TODO just guessing might be wrong
    assert not surf.neighbor

    # Geomeppy IDF doesnt check for valididty, but this method should.. -> ie that the surface matches a zone..


def test_create_subsurface_interior(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurface, partner_suburface = create_subsurface_for_interior_edge(
        zone_edge, door_details, case.zones, case.idf
    )
    assert room1.name in subsurface.subsurface_name
    assert room2.name in partner_suburface.subsurface_name


def test_create_subsurface_exterior(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurface = create_subsurface_for_exterior_edge(
        zone_drn_edge, window_details, case.zones, case.idf
    )
    assert room1.name in subsurface.subsurface_name


def test_sorting_directed_edges():
    edge = Edge("EAST", room1.name)
    expected_edge = (room1.name, WallNormal.EAST)
    assert expected_edge == edge.sorted_directed_edge


# TODO move to utils4plans!
def test_flatten_map_dummy_inputs():
    details_map = {1: [1, 2], 2: [3, 4], 3: [5, 6]}
    expected = [(1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (3, 6)]
    result = flatten_dict_map(details_map)
    assert expected == result


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    subsurface = create_subsurface_for_exterior_edge(
        zone_drn_edge, window_details, case.zones, case.idf
    )
    dom = subsurface
    print(dom)
    pass
    # subsurfaces = create_subsurfaces(edges, details, details_map, case.zones, case.idf)
    # int_flat = chain_flatten(interior_subsurfaces)
    # res = int_flat + exterior_subsurfaces

    # pass
