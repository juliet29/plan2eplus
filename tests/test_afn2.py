from replan2eplus.ex.afn import AFNExampleCases, AFNCaseDefinition

# from replan2eplus.ezcase.ez import EZ
from replan2eplus.ops.afn.logic import get_avail_zones
import pytest
from rich import print


@pytest.mark.parametrize("case", AFNExampleCases().list)
def test_get_avail_zones(case: AFNCaseDefinition):
    active_case = case.case_with_subsurfaces
    zones = get_avail_zones(active_case.objects.zones)
    print(zones)


if __name__ == "__main__":
    case = AFNExampleCases.A_ew
    active_case = case.case_with_subsurfaces
    a = 1 + 1

    #     zones = get_avail_zones(active_case.objects.zones)
    #     print(zones)

    # test_get_avail_zones(AFNExampleCases.A_ns)
