from replan2eplus.ezobjects.afn import AirflowNetwork
from replan2eplus.ezobjects.airboundary import Airboundary
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ezobjects.surface import Surface
from typing import NamedTuple, Sequence

from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.ortho_domain import OrthoDomain


def get_domains(items: Sequence[Surface | Subsurface | Airboundary]):
    domains: list[Domain] = []
    for item in items:
        if isinstance(item.domain, OrthoDomain):
            raise Exception(
                f"{item.display_name} has an orthogonal domain, but expected it to have a rectangular domain for plotting: {item}"
            )
        domains.append(item.domain)
    return domains


def get_edges(items: Sequence[Subsurface | Airboundary]):
    return [i.edge for i in items]


class SurfaceOrg(NamedTuple):
    non_afn_surfaces: list[Surface | Subsurface]
    windows: list[Subsurface]
    doors: list[Subsurface]
    airboundaries: list[Airboundary]


def organize_subsurfaces_and_surfaces(
    afn: AirflowNetwork, airboundaries: list[Airboundary], subsurfaces: list[Subsurface]
):
    non_afn_surfaces = [i.surface for i in afn.non_afn_airboundaries(airboundaries)]
    not_in_afn = non_afn_surfaces + afn.non_afn_subsurfaces(subsurfaces)

    # TODO this is an experiment -> will keep w/ list comprehensions for now..
    windows = filter(lambda x: x.is_window, afn.subsurfaces)
    doors = filter(lambda x: x.is_door, afn.subsurfaces)

    return SurfaceOrg(not_in_afn, list(windows), list(doors), afn.airboundaries)


class ConnectionOrg(NamedTuple):
    baseline: list[Airboundary | Subsurface]
    afn: list[Subsurface | Airboundary]


def organize_connections(
    afn: AirflowNetwork, airboundaries: list[Airboundary], subsurfaces: list[Subsurface]
):
    # doesnt filter because both the baseline and afn objects get plotted..
    return ConnectionOrg(airboundaries + subsurfaces, afn.surfacelike_objects)
