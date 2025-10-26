from copy import deepcopy
from replan2eplus.ex.afn import AFNExampleCases, AFNCaseDefinition

# from replan2eplus.ezcase.ez import EZ
from replan2eplus.ex.main import Interfaces
from replan2eplus.ops.afn.logic import (
    check_surfaces_for_nbs,
    determine_afn_objects,
    get_avail_afn_zones,
    get_avail_surfaces,
    get_avail_zones,
    update_zones,
)
from geomeppy import IDF
import pytest
from rich import print

from replan2eplus.ops.afn.presentation import create_afn_objects, select_afn_objects
from replan2eplus.ops.afn.writer import IDFAFNSurface, IDFAFNZone


@pytest.mark.parametrize("case", AFNExampleCases().list)
def test_get_avail_zones(case: AFNCaseDefinition):
    active_case = case.case_with_subsurfaces
    zones = get_avail_zones(active_case.objects.zones)

    assert len(zones) == case.n_zones_with_two_plus_valid_surfaces


@pytest.mark.parametrize("case", AFNExampleCases().list)
def test_get_avail_subsurfaces(case: AFNCaseDefinition):
    active_case = case.case_with_subsurfaces
    avail_zones = get_avail_zones(active_case.objects.zones)
    avail_subsurfaces = get_avail_surfaces(active_case.objects.subsurfaces, avail_zones)
    assert len(avail_subsurfaces.to_list()) == case.n_surfaces_in_avail_zones


@pytest.mark.parametrize("case", AFNExampleCases().list)
def test_filter_subsurfaces(case: AFNCaseDefinition):
    active_case = case.case_with_subsurfaces
    avail_zones = get_avail_zones(active_case.objects.zones)
    res = get_avail_surfaces(active_case.objects.subsurfaces, avail_zones).pipe(
        check_surfaces_for_nbs
    )
    assert len(res) == case.n_surfaces_after_check_nbs


@pytest.mark.parametrize("case_", AFNExampleCases().list)
def test_get_afn_objects(case_: AFNCaseDefinition):
    case = case_.case_with_subsurfaces
    zones, surfs = determine_afn_objects(case.objects.zones, case.objects.subsurfaces)
    assert len(zones) == case_.n_zones_in_afn
    assert len(surfs) == case_.n_surfs_in_afn


def test_selecting_afn_zones():
    case_ = AFNExampleCases().B_ne
    case = case_.case_with_subsurfaces
    afn_holder, _ = select_afn_objects(case.objects.zones, case.objects.subsurfaces, [])
    assert len(afn_holder.zones) == case_.n_zones_in_afn
    assert afn_holder.zones[0].room_name == Interfaces.rooms.r1.name


@pytest.mark.xfail()  #
def test_selecting_afn_surfaces():
    case_ = AFNExampleCases().B_ne
    case = case_.case_with_subsurfaces
    afn_holder, _ = select_afn_objects(case.objects.zones, case.objects.subsurfaces, [])
    assert len(afn_holder.subsurfaces) == case_.n_surfs_in_afn


def test_adding_afn_objects():
    case_ = AFNExampleCases().B_ne
    case = case_.case_with_subsurfaces
    _ = create_afn_objects(case.idf, case.objects.zones, case.objects.subsurfaces, [])
    print(case.idf.idfobjects["AIRFLOWNETWORK:MULTIZONE:SURFACE"])

    surfs = IDFAFNSurface.read(case.idf)
    assert len(surfs) == case_.n_surfs_in_afn

    zones = IDFAFNZone.read(case.idf)
    assert len(zones) == case_.n_zones_in_afn


def reg_test():
    def study(case_: AFNCaseDefinition):
        print(case_.name)
        case = case_.case_with_subsurfaces
        zones, surfs = determine_afn_objects(
            case.objects.zones, case.objects.subsurfaces
        )

        print(f"found_zones: {[i.room_name for i in zones]}")

    for case in AFNExampleCases().list:
        study(case)


if __name__ == "__main__":
    test_adding_afn_objects()
