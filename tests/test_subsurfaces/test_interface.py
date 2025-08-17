from replan2eplus.subsurfaces.presentation import create_subsurfaces
from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.examples.subsurfaces import test_simple, test_three_details


def test_creating_subsurfaces_simple(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurfaces = create_subsurfaces(test_simple.inputs, case.zones, case.idf)
    assert len(subsurfaces) == 3

def test_creating_subsurfaces_three_details(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurfaces = create_subsurfaces(test_three_details.inputs, case.zones, case.idf)
    assert len(subsurfaces) == 5

if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    subsurfaces = create_subsurfaces(test_three_details.inputs, case.zones, case.idf)
    assert len(subsurfaces) == 3
