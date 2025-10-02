from replan2eplus.examples.cases.minimal import get_minimal_case_with_rooms
from utils4plans.sets import set_intersection
from replan2eplus.idfobjects.variables import default_variables


def test_add_outputs(get_pytest_minimal_case):
    case = get_pytest_minimal_case
    test_vars = ["AFN Node Total Pressure", "Site Wind Direction"]
    case.idf.add_output_variables(test_vars)
    assert set_intersection(case.idf.get_output_variables(), test_vars)


def test_add_default_variables(get_pytest_minimal_case):
    case = get_pytest_minimal_case
    case.idf.add_output_variables(default_variables)
    test_vars = [
        "AFN Linkage Node 1 to Node 2 Volume Flow Rate",
        "AFN Zone Mixing Volume",
        "Site Wind Direction",
    ]
    assert set_intersection(case.idf.get_output_variables(), test_vars)


if __name__ == "__main__":
    print(default_variables)
    # case = get_minimal_case_with_rooms()
    # test_vars = ["AFN Node Total Pressure", "Site Wind Direction"]
    # case.idf.add_output_variables(test_vars)
    # print(case.idf.get_output_variables())
    # assert set_intersection(case.idf.get_output_variables(), test_vars)
