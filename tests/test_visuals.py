from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.visuals.base_plot import BasePlot


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    # case.idf.print_idf()
    # case.idf.idf.view_model()
    north_surfaces = [i for i in case.surfaces if i.direction.name == "NORTH" or i.direction.name == "EAST" or i.direction.name == "WEST"]
    bp = (
        BasePlot(case.zones)
        .plot_zones()
        .plot_zone_names()
        .plot_cardinal(cardinal_expansion_factor=1.3)
        .plot_surfaces(north_surfaces)
        .show()
    )
