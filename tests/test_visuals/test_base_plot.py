from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.visuals.base_plot import BasePlot
from replan2eplus.examples.subsurfaces import (
    simple_subsurface_inputs,
    three_details_subsurface_inputs,
)
from replan2eplus.subsurfaces.utils import get_unique_subsurfaces


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    case.add_subsurfaces(simple_subsurface_inputs.inputs)

    # get_unique_subsurfaces(case.subsurfaces)

    bp = (
        BasePlot(case.zones, cardinal_expansion_factor=1.8)
        .plot_zones()
        .plot_zone_names()
        .plot_cardinal()
        .plot_subsurfaces(case.subsurfaces)
        .plot_connections(case.subsurfaces)  # would be good to specify the color here.
    )

    # afn plot..
    case.add_airflownetwork()
    bp.plot_connections(case.airflownetwork.surfacelike_objects, color="blue", opacity=1, linewidth=2)
    bp.show()
