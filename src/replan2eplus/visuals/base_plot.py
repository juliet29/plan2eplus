from dataclasses import dataclass

import matplotlib.pyplot as plt

from replan2eplus.ezobjects.afn import AirflowNetwork
from replan2eplus.ezobjects.airboundary import Airboundary
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.visuals.domain_modifications import (
    compute_multidomain,
)
from replan2eplus.geometry.contact_points import calculate_cardinal_points
from replan2eplus.visuals.axis_modifications import (
    AnnotationPair,
    add_annotations,
    add_connection_lines,
    add_rectangles,
    add_surface_lines,
)
from replan2eplus.visuals.domain_modifications import expand_domain
from replan2eplus.visuals.organize import (
    organize_connections,
    organize_subsurfaces_and_surfaces,
)
from replan2eplus.visuals.styles.artists import (
    AnnotationStyles,
    ConnectionStyles,
    RectangleStyles,
    SurfaceStyles,
)
from replan2eplus.visuals.transform import (
    EXPANSION_FACTOR,
)  # TODO move this to a config!


@dataclass
class BasePlot:
    zones: list[Zone]
    cardinal_expansion_factor: float = EXPANSION_FACTOR
    extents_expansion_factor: float = EXPANSION_FACTOR

    def __post_init__(self):
        self.fig, self.axes = plt.subplots(figsize=(12, 8))
        self.total_domain = compute_multidomain([i.domain for i in self.zones])

        self.cardinal_domain = expand_domain(
            self.total_domain, self.cardinal_expansion_factor
        )
        self.extents = expand_domain(
            self.cardinal_domain, self.extents_expansion_factor
        )

    def plot_zones(self, style=RectangleStyles()):
        add_rectangles(
            [i.domain for i in self.zones], [style], self.axes
        )  # TODO if pass a list of styles, then apply each differently -> when are doing values .. or just have different function for if have values..
        return self

    def plot_zone_names(self, style=AnnotationStyles()):
        add_annotations(
            [AnnotationPair(i.domain.centroid, i.room_name) for i in self.zones],
            style,
            self.axes,
        )
        return self

    def plot_cardinal_names(self, style=AnnotationStyles()):
        cardinal_points = calculate_cardinal_points(self.cardinal_domain)
        add_annotations(
            [
                AnnotationPair(value, key)
                for key, value in cardinal_points.dict_.items()
            ],
            style,
            self.axes,
        )
        return self

    def plot_subsurfaces_and_surfaces(
        self,
        afn: AirflowNetwork,
        airboundaries: list[Airboundary],
        subsurfaces: list[Subsurface],
        style=SurfaceStyles(),
    ):
        surface_org = organize_subsurfaces_and_surfaces(afn, airboundaries, subsurfaces)
        add_surface_lines(
            [i.domain for i in surface_org.non_afn_surfaces],
            style.non_afn_surfaces,
            self.axes,
        )
        add_surface_lines(
            [i.domain for i in surface_org.windows], style.windows, self.axes
        )
        add_surface_lines([i.domain for i in surface_org.doors], style.doors, self.axes)
        add_surface_lines(
            [i.surface.domain for i in surface_org.airboundaries],
            style.airboundaries,
            self.axes,
        )
        return self

    def plot_connections(
        self,
        afn: AirflowNetwork,
        airboundaries: list[Airboundary],
        subsurfaces: list[Subsurface],
        style=ConnectionStyles(),
    ):
        connections_org = organize_connections(afn, airboundaries, subsurfaces)
        # TODO: can make cleaner w/ zip..
        add_connection_lines(
            [i.domain for i in connections_org.baseline],
            [i.edge for i in connections_org.baseline],
            self.zones,
            calculate_cardinal_points(self.cardinal_domain),
            [style.baseline],
            self.axes,
        )
        add_connection_lines(
            [i.domain for i in connections_org.afn],
            [i.edge for i in connections_org.afn],
            self.zones,
            calculate_cardinal_points(self.cardinal_domain),
            [style.afn],
            self.axes,
        )
        return self

    def show(self):
        self.axes.set_xlim(self.extents.horz_range.as_tuple)
        self.axes.set_ylim(self.extents.vert_range.as_tuple)
        self.axes.legend()

        plt.show()
