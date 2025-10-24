import pytest

from replan2eplus.ex.main import Cases
from replan2eplus.ex.main import Interfaces as UI

from replan2eplus.idfobjects.base import get_names_of_idf_objects
from replan2eplus.ops.zones.create import create_zones
from replan2eplus.ops.zones.idfobject import IDFZone


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
    case = Cases().ep_afn
    n_zones = len(case.objects.zones)
    assert n_zones == 3


@pytest.mark.xfail()
def test_get_zone_subsurfaces(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    zone = case.zones[0]
    assert len(zone.subsurface_names) == 2


def test_update_zone_name():
    case = Cases().two_room
    zone_name = "Block `room1` Storey 0"
    test_name = "test_name"
    IDFZone().update(case.idf, zone_name, "Name", test_name)
    new_zones = IDFZone().read(case.idf)
    assert test_name in get_names_of_idf_objects(new_zones)
    # zone1 = true_zones[0]
    # zone1["Name"] =


if __name__ == "__main__":
    # zones = IDFZone.read(case.idf)[0]
    test_update_zone_name()
    # case = EZ()
    # rooms = [UI.rooms.r1, UI.rooms.r2]
    # zones = create_zones(case.idf, rooms)

    # ss = z.subsurface_names
    # print(ss)
    # idf = get_minimal_idf()
    # zones, surfaces = create_zones(idf, test_rooms)
    # print(surfaces)
    # # EZObject2D(epbunch=)
