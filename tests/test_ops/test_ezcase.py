from rich import print
import pytest

from replan2eplus.ex.afn import AFNEdgeGroups as AFNEdgeGroups, AFNExampleCases
from replan2eplus.ex.make import make_test_case
from replan2eplus.ex.make import airboundary_edges

from replan2eplus.ezcase.ez import EZ, ep_paths
from replan2eplus.ops.afn.create import AFNInput
from replan2eplus.ops.afn.utils.venting import AFNVentingInput
from replan2eplus.ops.schedules.interfaces.year import create_year_from_single_value
from replan2eplus.paths import DynamicPaths
from replan2eplus.ex.schedule import ExampleYear


@pytest.mark.slow
def test_case_basic():
    case = make_test_case(AFNEdgeGroups.A_ew)
    case.save_and_run(run=True)
    assert 1


@pytest.mark.slow
def test_case_airboudary():
    case = make_test_case(AFNEdgeGroups.A_ns, airboundary_edges)
    case.save_and_run(run=True)
    assert 1


def test_case_airboundary_afn():
    case = make_test_case(AFNEdgeGroups.A_ns, airboundary_edges, afn=True)
    case.save_and_run(run=True)
    assert 1


def test_run_case_without_reading():
    path = DynamicPaths.afn_examples / AFNExampleCases.A_ew.name / ep_paths.idf_name
    case = EZ(path, read_existing=False)
    case.save_and_run(DynamicPaths.THROWAWAY_PATH, ep_paths.default_weather, run=True)
    assert 1


def test_case_with_afn_venting():
    venting_input = AFNVentingInput("Doors", ExampleYear().year)
    case = make_test_case(
        AFNEdgeGroups.A_ns, afn=True, afn_input=AFNInput([venting_input])
    )
    case.save_and_run(run=True)
    assert 1


def test_case_with_afn_no_venting():
    closed_year = create_year_from_single_value(0)
    venting_input = AFNVentingInput("Doors", closed_year)
    case = make_test_case(
        AFNEdgeGroups.A_ns, afn=True, afn_input=AFNInput([venting_input])
    )
    case.save_and_run(run=False)
    # assert 1

# TODO!
# ortho domains..
# running from an existing idf -> to run don't need to read an idf really, that is just needed for graphing.. so maybe reading existing objects is a flag that can get turned on or off.. if adding new things, should read ..


if __name__ == "__main__":
    # case = make_test_case(AFNEdgeGroups.A_ns, airboundary_edges, afn=True)
    test_case_with_afn_no_venting()
    # case.save_and_run(run=True)
