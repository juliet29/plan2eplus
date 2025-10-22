import pytest

from replan2eplus.ex.main import Cases
from replan2eplus.ex.main import UserInterfaces as UI

from replan2eplus.ops.zones.create import create_zones


def test_zone_names():
    case = Cases().two_room
    zones = case.objects.zones
    assert set([i.room_name for i in zones]) == set(
        [i.name for i in UI.rooms.two_room_list]
    )


def test_add_zones():
    case = Cases().base
    zones, *_ = create_zones(case.idf, UI.rooms.two_room_list)
    assert len(zones) == len(UI.rooms.two_room_list)


def test_add_surfaces_with_zones():
    case = Cases().base
    _, surfaces = create_zones(case.idf, UI.rooms.two_room_list)
    N_SURFACES_PER_CUBE = 6
    assert len(surfaces) == len(UI.rooms.two_room_list) * N_SURFACES_PER_CUBE


def test_read():
    case = Cases().example
    n_zones = len(case.objects.zones)
    assert n_zones == 3



@pytest.mark.xfail()
def test_get_zone_subsurfaces(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    zone = case.zones[0]
    assert len(zone.subsurface_names) == 2


if __name__ == "__main__":
    test_read()
    # case = EZ()
    # rooms = [UI.rooms.r1, UI.rooms.r2]
    # zones = create_zones(case.idf, rooms)

    # ss = z.subsurface_names
    # print(ss)
    # idf = get_minimal_idf()
    # zones, surfaces = create_zones(idf, test_rooms)
    # print(surfaces)
    # # EZObject2D(epbunch=)
