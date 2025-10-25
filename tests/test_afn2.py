from copy import deepcopy
from replan2eplus.ex.afn import AFNExampleCases, AFNCaseDefinition

# from replan2eplus.ezcase.ez import EZ
from replan2eplus.ops.afn.logic import (
    check_surfaces_for_nbs,
    get_avail_subsurfaces,
    get_avail_zones,
    update_zones,
)

import pytest
from rich import print


@pytest.mark.parametrize("case", AFNExampleCases().list)
def test_get_avail_zones(case: AFNCaseDefinition):
    active_case = case.case_with_subsurfaces
    zones = get_avail_zones(active_case.objects.zones)

    assert len(zones) == case.n_zones_with_two_plus_valid_surfaces


@pytest.mark.parametrize("case", AFNExampleCases().list)
def test_get_avail_subsurfaces(case: AFNCaseDefinition):
    active_case = case.case_with_subsurfaces
    avail_zones = get_avail_zones(active_case.objects.zones)
    avail_subsurfaces = get_avail_subsurfaces(
        active_case.objects.subsurfaces, avail_zones
    )
    assert len(avail_subsurfaces.to_list()) == case.n_surfaces_in_avail_zones


@pytest.mark.parametrize("case", AFNExampleCases().list)
def test_filter_subsurfaces(case: AFNCaseDefinition):
    active_case = case.case_with_subsurfaces
    avail_zones = get_avail_zones(active_case.objects.zones)
    res = get_avail_subsurfaces(active_case.objects.subsurfaces, avail_zones).pipe(
        check_surfaces_for_nbs
    )
    assert len(res) == case.n_surfaces_after_check_nbs


def reg_test():
    def study(case: AFNCaseDefinition):
        print(case.name)
        active_case = case.case_with_subsurfaces
        avail_zones = get_avail_zones(active_case.objects.zones)
        # print(f"avail_zones: {avail_zones}")

        avail_surfs = get_avail_subsurfaces(
            active_case.objects.subsurfaces, avail_zones
        ).pipe(check_surfaces_for_nbs)
        print(f"avail_surfs1: {avail_surfs}")
        print(f"avail_surfs1 again: {avail_surfs}")

        avail_zones2 = update_zones(avail_zones, avail_surfs)
        print(f"avail zones2 {avail_zones2}")

        # pipe(
        #     get_avail_zones(active_case.objects.zones),
        #     get_avail_subsurfaces(active_case.objects.subsurfaces, avail_zones).pipe(
        #         check_surfaces_for_nbs
        #     ),
        #     update_zones(avail_zones, avail_surfs),
        # )

    for case in AFNExampleCases().list:
        study(case)


if __name__ == "__main__":
    reg_test()
