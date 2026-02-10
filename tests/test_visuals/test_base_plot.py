from plan2eplus.ex.afn import AFNEdgeGroups as AFNEdgeGroups

# from plan2eplus.examples.ortho_domain import (
#     create_ortho_case,
# )
from plan2eplus.ex.make import airboundary_edges, make_base_plot, make_test_case


def test_make_base_plot():
    case = make_test_case(AFNEdgeGroups.A_ew, afn=True)
    make_base_plot(case)
    assert 1
    # TODO -> make better tests, check the matplotlib axes..


# def test_make_ortho_plot():
#     case = create_ortho_case()
#     make_base_plot(case)
#     assert 1


if __name__ == "__main__":
    case = make_test_case(AFNEdgeGroups.D, afn=True)
    bp = make_base_plot(case)
    bp.show()
