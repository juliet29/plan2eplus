from replan2eplus.afn.presentation import create_afn_objects, select_afn_objects
from replan2eplus.airboundary.presentation import update_airboundary_constructions
from replan2eplus.examples.subsurfaces import (
    door_details,
    room1,
    zone_drn_edge,
    zone_edge,
    zone_drn_edge_room2,
)
from replan2eplus.subsurfaces.presentation import (
    create_subsurface_for_exterior_edge,
)
from replan2eplus.examples.minimal import get_minimal_case_with_rooms

# TODO add an image of this!!! -> make a reference for all the examples -> md file?


# TODO parametrize this so can test the more complex subsurface situation at the same tme..
def test_selecting_afn_objects(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    afn_inputs = select_afn_objects(case.zones, case.subsurfaces, [])
    assert len(afn_inputs.zones) == 1
    assert room1.name == afn_inputs.zones_[0].room_name
    assert len(afn_inputs.subsurfaces) == 2



def test_adding_afn_objects(get_pytest_minimal_case_with_subsurfaces):
    """
    # expect 1 sim control object, 1 zone, (2 subsurfaces -> 1 surface, 1 opening each -> 2x2 = 4)
    # expect 6 objects in total
    """
    case = get_pytest_minimal_case_with_subsurfaces
    create_afn_objects(case.idf, case.zones, case.subsurfaces, [])
    afn_objects = case.idf.get_afn_objects()
    assert len(afn_objects) == 6


def test_selecting_afn_objects_from_case_with_airboundary_two_doors(
    get_pytest_minimal_case_with_rooms,
):
    case = get_pytest_minimal_case_with_rooms
    case.add_airboundaries([zone_edge])

    # TODO replace using API!
    surf_1 = create_subsurface_for_exterior_edge(
        zone_drn_edge, door_details, case.zones, case.idf
    )
    surf_2 = create_subsurface_for_exterior_edge(
        zone_drn_edge_room2, door_details, case.zones, case.idf
    )
    case.subsurfaces = [surf_1, surf_2]
    afn_inputs = select_afn_objects(case.zones, case.subsurfaces, case.airboundaries)

    assert len(afn_inputs.zones) == 2
    assert room1.name == afn_inputs.zones_[0].room_name
    assert len(afn_inputs.subsurfaces) == 2
    assert len(afn_inputs.surfaces) == 1


def test_selecting_afn_objects_from_case_with_airboundary_one_door(
    get_pytest_minimal_case_with_rooms,
):
    case = get_pytest_minimal_case_with_rooms
    case.add_airboundaries([zone_edge])

    surf_1 = create_subsurface_for_exterior_edge(
        zone_drn_edge, door_details, case.zones, case.idf
    )
    case.subsurfaces = [surf_1]
    afn_inputs = select_afn_objects(case.zones, case.subsurfaces, case.airboundaries)

    assert len(afn_inputs.zones) == 1
    assert room1.name == afn_inputs.zones_[0].room_name
    assert len(afn_inputs.subsurfaces) == 1
    assert len(afn_inputs.surfaces) == 1




if __name__ == "__main__":
    pass
