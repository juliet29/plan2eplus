from rich import print
import pytest

from replan2eplus.ex.afn import EdgeGroups as AFNEdgeGroups
from replan2eplus.ex.make import make_test_case
from replan2eplus.ex.make import airboundary_edges


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


# TODO!
# ortho domains..
# running from an existing idf -> to run don't need to read an idf really, that is just needed for graphing.. so maybe reading existing objects is a flag that can get turned on or off.. if adding new things, should read ..


if __name__ == "__main__":
    case = make_test_case(AFNEdgeGroups.A_ns, airboundary_edges, afn=True)
    case.save_and_run(run=True)
