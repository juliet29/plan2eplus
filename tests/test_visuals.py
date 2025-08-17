from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.visuals.base_plot import BasePlot


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    # case.idf.print_idf()
    bp = (
        BasePlot(case.zones, case.surfaces)
        .plot_zones()
        .plot_zone_names()
        .plot_cardinal()
        .show()
    )
