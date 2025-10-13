from replan2eplus.ezcase.main import EZCase
from replan2eplus.ezcase.read import ExistCase
from replan2eplus.visuals.base.base_plot import BasePlot


def make_base_plot(case: EZCase | ExistCase):

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

    return bp
