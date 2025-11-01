from replan2eplus.ex.afn import AFNExampleCases
from replan2eplus.ops.afn.create import create_afn_objects
from replan2eplus.ops.afn.idfobject import IDFAFNSurface
from replan2eplus.ex.afn import AFNEdgeGroups as AFNEdgeGroups, AFNExampleCases
from replan2eplus.ex.make import make_test_case
from replan2eplus.ops.afn.utils.coefficients import assign_external_nodes


def test_match_external_nodes():
    case = make_test_case(AFNEdgeGroups.A_ew, afn=True)
    assign_external_nodes(case.idf, case.objects.airflow_network.subsurfaces)


if __name__ == "__main__":
    test_match_external_nodes()
