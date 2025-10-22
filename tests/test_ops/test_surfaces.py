from replan2eplus.ex.main import Cases
from replan2eplus.ops.surfaces.idfobject import IDFSurface

from rich import print
# TODO: test init surface!

def test_surface_idf():
    case = Cases().two_room
    surfaces = IDFSurface.read(case.idf)
    print(surfaces)
    print(case.objects.surfaces)
    return surfaces



# def test_assign_surface_conditions(get_pytest_example_idf):
#     idf = get_pytest_example_idf
#     surfaces = idf.get_surfaces()
#     outward_surfaces = [
#         i for i in surfaces if i.Outside_Boundary_Condition == "outdoors"
#     ]
#     s1 = Surface(outward_surfaces[0])
#     assert s1.boundary_condition == "outdoors"


# def test_get_surface_neighbor(get_pytest_example_idf):
#     idf = get_pytest_example_idf
#     surfaces = [Surface(i) for i in idf.get_surfaces()]
#     indoor_surfaces = [i for i in surfaces if i.boundary_condition == "surface"]

#     assert indoor_surfaces[0].neighbor

    


if __name__ == "__main__":
    test_surface_idf()
