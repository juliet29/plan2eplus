from replan2eplus.examples.minimal import get_minimal_case_with_rooms
from replan2eplus.visuals2.plot import BasePlot
from replan2eplus.examples.subsurfaces import (
    simple_subsurface_inputs,
    three_details_subsurface_inputs,
)
from replan2eplus.subsurfaces.utils import get_unique_subsurfaces


if __name__ == "__main__":
    case = get_minimal_case_with_rooms()
    case.add_subsurfaces(simple_subsurface_inputs.inputs)
    case.add_airflownetwork()

    # get_unique_subsurfaces(case.subsurfaces)

    bp = (
        BasePlot(case.zones, cardinal_expansion_factor=1.8)
        .plot_zones()
        .plot_zone_names()
        .plot_cardinal_names()
        .plot_subsurfaces_and_surfaces(
            case.airflownetwork, case.unique_airboundaries, case.unique_subsurfaces
        )
        .plot_connections(
            case.airflownetwork, case.unique_airboundaries, case.unique_subsurfaces
        )  # would be good to specify the color here.
    )

    bp.show()
