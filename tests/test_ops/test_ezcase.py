import pytest

from plan2eplus.ex.afn import AFNEdgeGroups as AFNEdgeGroups, AFNExampleCases
from plan2eplus.ex.make import make_test_case
from plan2eplus.ex.make import airboundary_edges

from plan2eplus.ezcase.ez import EZ, ep_paths
from plan2eplus.ops.afn.create import AFNInput
from plan2eplus.ops.afn.utils.venting import AFNVentingInput
from plan2eplus.ops.schedules.interfaces.year import create_year_from_single_value
from plan2eplus.paths import DynamicPaths
from plan2eplus.ex.schedule import ExampleYear
from plan2eplus.results.sql import get_qoi
import numpy as np


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


QUANTILES = [0.1, 0.25, 0.75, 0.9]


def test_case_with_default_venting():
    opath = DynamicPaths.ts_open
    case = make_test_case(AFNEdgeGroups.A_ns, afn=True, output_path=opath)
    case.save_and_run(run=False, output_path=opath)
    res = get_qoi("AFN Zone Ventilation Volume", opath)

    res2 = get_qoi("AFN Surface Venting Availability Status", opath)

    quantiles = res2.data_arr.mean("space_names").quantile(q=QUANTILES)
    assert np.unique(quantiles.data) == np.array(1)


def test_case_with_afn_venting():
    opath = DynamicPaths.ts_dynamic
    venting_input = AFNVentingInput("Doors", ExampleYear().year)
    case = make_test_case(
        AFNEdgeGroups.A_ns,
        afn=True,
        output_path=opath,
        afn_input=AFNInput([venting_input]),
    )
    case.save_and_run(run=False, output_path=opath)
    res = get_qoi("AFN Zone Ventilation Volume", opath)
    res2 = get_qoi("AFN Surface Venting Availability Status", opath)

    quantiles = res2.data_arr.mean("space_names").quantile(q=QUANTILES)
    assert np.array_equal(np.unique(quantiles.data), np.array([0, 1]))


def test_case_with_afn_no_venting():
    opath = DynamicPaths.ts_closed
    closed_year = create_year_from_single_value(0)
    venting_input = AFNVentingInput("Doors", closed_year)
    case = make_test_case(
        AFNEdgeGroups.A_ns,
        afn=True,
        output_path=opath,
        afn_input=AFNInput([venting_input]),
    )
    case.save_and_run(run=False, output_path=opath)
    res = get_qoi("AFN Zone Ventilation Volume", opath)
    res2 = get_qoi("AFN Surface Venting Availability Status", opath)

    # assert 1
    quantiles = res2.data_arr.mean("space_names").quantile(q=QUANTILES)
    assert np.unique(quantiles.data) == np.array(0)


# TODO!
# ortho domains..
# running from an existing idf -> to run don't need to read an idf really, that is just needed for graphing.. so maybe reading existing objects is a flag that can get turned on or off.. if adding new things, should read ..


if __name__ == "__main__":

    # case = make_test_case(AFNEdgeGroups.A_ns, airboundary_edges, afn=True)
    r = test_case_with_default_venting()
    t = test_case_with_afn_venting()
    y = test_case_with_afn_no_venting()
    # print(r, t[0], t[1], y)
    # arr = t[2].data_arr
    # print(np.unique(arr.data))
    #
    # # case.save_and_run(run=True)
