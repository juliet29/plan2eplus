from replan2eplus.examples.subsurfaces import get_minimal_case_with_subsurfaces, e0, e1
from replan2eplus.ezcase.read import ExistCase, get_geom_objects


def test_read_geom_objects(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    zones, surfaces, subsurfaces = get_geom_objects(case.idf)
    expected_edges = set([e1.as_tuple, e1.as_tuple])
    result_edges = set([i.edge.as_tuple for i in subsurfaces])
    assert result_edges.intersection(expected_edges)


if __name__ == "__main__":
    case = get_minimal_case_with_subsurfaces()
    zones, surfaces, subsurfaces = get_geom_objects(case.idf)
    # print(subsurfaces[0])
    print([i.edge for i in subsurfaces])
    print([i.edge.as_tuple for i in subsurfaces])
    zones, surfaces, subsurfaces = get_geom_objects(case.idf)
    expected_edges = set([e0.as_tuple, e1.as_tuple])
    result_edges = set([i.edge.as_tuple for i in subsurfaces])
    check = result_edges.intersection(expected_edges)
    print(check)
