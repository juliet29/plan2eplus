from replan2eplus.examples.plots.base_plot import make_base_plot
from replan2eplus.examples.cases.afn_case import (
    make_afn_case,
)
from replan2eplus.examples.ortho_domain import (
    create_ortho_case,
)


def test_make_base_plot():
    case = make_afn_case()
    make_base_plot(case)
    assert 1
    # TODO -> make better tests, check the matplotlib axes..


def test_make_ortho_plot():
    case = create_ortho_case()
    make_base_plot(case)
    assert 1


if __name__ == "__main__":
    case = create_ortho_case()
    bp = make_base_plot(case)
    bp.show()
