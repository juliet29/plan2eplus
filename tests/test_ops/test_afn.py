from replan2eplus.ops.afn.presentation import create_afn_objects, select_afn_objects
# from replan2eplus.ops.afn.utils import get_idf_objects_from_afn_surface_names
from replan2eplus.ops.subsurfaces.logic.exterior import (
    create_subsurface_for_exterior_edge,
)
from replan2eplus.ex.main import Cases, Interfaces
# TODO add an image of this!!! -> make a reference for all the examples -> md file?


# TODO parametrize this so can test the more complex subsurface situation at the same tme..
def test_selecting_afn_objects():
    case = Cases().subsurfaces_simple
    afn_holder, _ = select_afn_objects(case.objects.zones, case.objects.subsurfaces, [], case.objects.surfaces)
    assert len(afn_holder.zones) == 1
    assert Interfaces.rooms.r1.name == afn_holder.zones[0].room_name
    assert len(afn_holder.subsurfaces) == 1


def test_adding_afn_objects(get_pytest_minimal_case_with_subsurfaces):
    """
    # expect 1 sim control object, 1 zone, (1 subsurfaces with 1 surface and 1 opening each -> 1x2 = 2)
    # expect 4 objects in total
    """
    case = get_pytest_minimal_case_with_subsurfaces
    create_afn_objects(case.idf, case.zones, case.subsurfaces, [], case.surfaces)
    afn_objects = case.idf.get_afn_objects()
    assert len(afn_objects) == 4


# def test_selecting_afn_objects_from_case_with_airboundary_two_doors(
#     get_pytest_minimal_case_with_rooms,
# ):
#     case = get_pytest_minimal_case_with_rooms
#     case.add_airboundaries([e0])

#     # TODO replace using API!
#     surf_1 = create_subsurface_for_exterior_edge(
#         zone_drn_edge, door_details, case.zones, case.idf
#     )
#     surf_2 = create_subsurface_for_exterior_edge(
#         zone_drn_edge_room2, door_details, case.zones, case.idf
#     )
#     case.subsurfaces = [surf_1, surf_2]
#     afn_inputs = select_afn_objects(
#         case.zones, case.subsurfaces, case.airboundaries, case.surfaces
#     )

#     assert len(afn_inputs.zones) == 2
#     assert room1.name == afn_inputs.zones_[0].room_name
#     assert len(afn_inputs.subsurfaces) == 2
#     assert len(afn_inputs.airboundaires) == 1


# def test_selecting_afn_objects_from_case_with_airboundary_one_door(
#     get_pytest_minimal_case_with_rooms,
# ):
#     case = get_pytest_minimal_case_with_rooms
#     case.add_airboundaries([e0])

#     surf_1 = create_subsurface_for_exterior_edge(
#         zone_drn_edge, door_details, case.zones, case.idf
#     )
#     case.subsurfaces = [surf_1]
#     afn_inputs = select_afn_objects(
#         case.zones, case.subsurfaces, case.airboundaries, case.surfaces
#     )

#     assert len(afn_inputs.zones) == 1
#     assert room1.name == afn_inputs.zones_[0].room_name
#     assert len(afn_inputs.subsurfaces) == 1
#     assert len(afn_inputs.airboundaires) == 0


# # TODO test the case when AFN subsurfaces shuld be excluded..


# def test_selecting_idf_afn_objects():
#     case = make_afn_case()
#     select_fx = lambda x: x
#     idf_objs = get_idf_objects_from_afn_surface_names(
#         case.idf,
#         case.airflownetwork,
#         select_fx,
#     )
#     assert len(idf_objs) == 4


# if __name__ == "__main__":
#     pass
