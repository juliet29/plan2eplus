from replan2eplus.examples.subsurfaces import get_minimal_case_with_subsurfaces, e0, e1
from replan2eplus.ezcase.read import ExistCase, get_geom_objects
from replan2eplus.geometry.coords import Coordinate3D
import pytest

from replan2eplus.geometry.plane import compute_unit_normal

# TODO this seems wrong location?? 

@pytest.mark.skip()
def test_read_geom_objects(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    zones, surfaces, subsurfaces = get_geom_objects(case.idf)
    expected_edges = set([e1.as_tuple, e1.as_tuple]) #  NOTE: the names are wrong -> now room names not plan names, so this will fail! but just for the studies
    result_edges = set([i.edge.as_tuple for i in subsurfaces])
    assert result_edges.intersection(expected_edges)
    assert len(zones[0].surfaces) == 6

def test_compute_unit_normal():
    coords = [Coordinate3D(x=3.71, y=10.54, z=0.0), Coordinate3D(x=3.71, y=8.26, z=0.0), Coordinate3D(x=2.01, y=8.26, z=0.0), Coordinate3D(x=2.01, y=10.54, z=0.0)]
    coords_tup = [i.as_three_tuple for i in coords]
    expected = "Z"
    result = compute_unit_normal(coords_tup)
    assert expected == result


if __name__ == "__main__":
    test_compute_unit_normal()
    # case = get_minimal_case_with_subsurfaces()
    # zones, surfaces, subsurfaces = get_geom_objects(case.idf)
    # # print(subsurfaces[0])
    # print([i.edge for i in subsurfaces])
    # print([i.edge.as_tuple for i in subsurfaces])
    # zones, surfaces, subsurfaces = get_geom_objects(case.idf)
    # expected_edges = set([e0.as_tuple, e1.as_tuple])
    # result_edges = set([i.edge.as_tuple for i in subsurfaces])
    # check = result_edges.intersection(expected_edges)
    # print(check)
    pass
