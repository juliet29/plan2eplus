from replan2eplus.subsurfaces.presentation import create_subsurfaces
from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.examples.subsurfaces import test_simple, test_three_details, room2
from replan2eplus.ezobjects.subsurface import Subsurface


def test_creating_subsurfaces_simple(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurfaces = create_subsurfaces(test_simple.inputs, case.zones, case.idf)
    assert len(subsurfaces) == 3


def test_creating_subsurfaces_three_details(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    subsurfaces = create_subsurfaces(test_three_details.inputs, case.zones, case.idf)
    assert len(subsurfaces) == 5


def test_subsurface_equality(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    eq_subsurfaces = [i for i in case.subsurfaces if i.edge.space_b == room2.name]
    assert len(eq_subsurfaces) == 2
    ss1, ss2 = eq_subsurfaces
    assert ss1 == ss2


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    subsurfaces = create_subsurfaces(test_simple.inputs, case.zones, case.idf)
    print(subsurfaces)

# TODO! stronger checks on tehse? rn just checking that get the right number of subsurfaces.. are they on the right faces?
