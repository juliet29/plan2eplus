from replan2eplus.afn.presentation import select_afn_objects
from replan2eplus.examples.subsurfaces import room1


# TODO parametrize this so can test the more complex subsurface situation at the same tme..
def test_afn_simple(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    zones, subsurfaces = select_afn_objects(case.zones, case.subsurfaces)
    assert len(zones) == 1
    assert room1.name == zones[0].room_name
    assert len(subsurfaces) == 2
