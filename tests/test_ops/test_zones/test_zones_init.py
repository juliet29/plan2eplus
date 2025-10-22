import pytest

from replan2eplus.ex.main import Cases
from replan2eplus.ex.main import UserInterfaces as UI

# from replan2eplus.examples.cases.minimal import get_minimal_idf, test_rooms
# from replan2eplus.examples.subsurfaces import get_minimal_case_with_subsurfaces
from replan2eplus.ezcase.ez import EZ
from replan2eplus.ops.zones.create import create_zones

N_SURFACES_PER_CUBE = 6


# ## NOTE: this stuff applies to most ep objects and might be moved
# def test_init_zone(get_pytest_example_idf):
#     idf = get_pytest_example_idf
#     zones = idf.get_zones()
#     zone = IDFZone(zones[0])
#     assert zone.expected_key == keys.ZONE  # TODO mayve test name?


# def test_init_zone_with_surface(get_pytest_example_idf):
#     with pytest.raises(InvalidEpBunchError) as excinfo:
#         idf = get_pytest_example_idf
#         surfaces = idf.get_surfaces()
#         IDFZone(surfaces[0])
#         assert "ZONE" in str(excinfo.value)


def test_zone_names():  # TODO more thorough test of names..
    case = Cases().two_room
    zones = case.objects.zones
    assert set([i.room_name for i in zones]) == set(
        [i.name for i in UI.rooms.two_room_list]
    )


## NOTE: This is more zone specific


def test_add_zones():
    case = Cases().base
    zones, *_ = create_zones(case.idf, UI.rooms.two_room_list)
    assert len(zones) == len(UI.rooms.two_room_list)


def test_add_surfaces_with_zones():
    case = Cases().base
    _, surfaces = create_zones(case.idf, UI.rooms.two_room_list)
    a = 1+1
    assert len(surfaces) == len(UI.rooms.two_room_list) * N_SURFACES_PER_CUBE


@pytest.mark.xfail()
def test_get_zone_subsurfaces(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    zone = case.zones[0]
    assert len(zone.subsurface_names) == 2


if __name__ == "__main__":
    # test_add_surfaces_with_zones()
    case = EZ()
    rooms = [UI.rooms.r1, UI.rooms.r2]
    zones = create_zones(case.idf, rooms)




    # ss = z.subsurface_names
    # print(ss)
    # idf = get_minimal_idf()
    # zones, surfaces = create_zones(idf, test_rooms)
    # print(surfaces)
    # # EZObject2D(epbunch=)
