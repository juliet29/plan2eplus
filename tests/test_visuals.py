from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.visuals.base_plot import BasePlot
from replan2eplus.examples.subsurfaces import test_simple, test_three_details
from replan2eplus.subsurfaces.utils import filter_subsurfaces


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    case.add_subsurfaces(test_simple.inputs)

    filter_subsurfaces(case.subsurfaces)

    # case.idf.print_idf()
    # case.idf.idf.view_model()
    north_surfaces = [
        i
        for i in case.surfaces
        if i.direction.name == "NORTH" or i.direction.name == "EAST"
    ]
    bp = (
        BasePlot(case.zones, cardinal_expansion_factor=1.8)
        .plot_zones()
        .plot_zone_names()
        .plot_cardinal()
        .plot_subsurfaces(case.subsurfaces)
        .plot_connections(case.subsurfaces)
        .show()
    )
