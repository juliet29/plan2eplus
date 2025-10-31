from replan2eplus.ex.afn import AFNExampleCases, AFNCaseDefinition
from replan2eplus.ezcase.ez import EZ, ep_paths


def test_ammend_afn_surface():
    case = AFNExampleCases.A_ew
    zones = get_avail_zones(active_case.objects.zones)