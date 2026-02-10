from plan2eplus.ops.afn.ezobject import AirflowNetwork
from plan2eplus.ops.airboundary.ezobject import Airboundary
from plan2eplus.ops.subsurfaces.ezobject import Subsurface
from plan2eplus.ops.surfaces.ezobject import Surface
from typing import NamedTuple, Sequence

from plan2eplus.geometry.domain import Domain
from plan2eplus.geometry.ortho_domain import OrthoDomain


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
    non_afn_surfaces: list[Airboundary | Subsurface]
    windows: list[Subsurface]
    doors: list[Subsurface]
    airboundaries: list[Airboundary]


def organize_subsurfaces_and_surfaces(
    afn: AirflowNetwork, airboundaries: list[Airboundary], subsurfaces: list[Subsurface]
):
    non_afn_surfaces = afn.get_non_afn_surfaces(airboundaries + subsurfaces)

    windows = filter(lambda x: x.is_window, afn.subsurfaces)
    doors = filter(lambda x: x.is_door, afn.subsurfaces)

    return SurfaceOrg(non_afn_surfaces, list(windows), list(doors), afn.airboundaries)


class ConnectionOrg(NamedTuple):
    baseline: list[Airboundary | Subsurface]
    afn: list[Subsurface | Airboundary]


def organize_connections(
    afn: AirflowNetwork, airboundaries: list[Airboundary], subsurfaces: list[Subsurface]
):
    # NOTE: doesnt filter because both the baseline and afn objects get plotted, they just get plotted with different markings 
    return ConnectionOrg(airboundaries + subsurfaces, afn.afn_surfaces)
