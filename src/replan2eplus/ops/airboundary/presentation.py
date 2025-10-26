from geomeppy import IDF

from replan2eplus.ops.airboundary.ezobject import Airboundary
from replan2eplus.ops.airboundary.idfobject import (
    IDFAirboundaryConstruction,
)
from replan2eplus.ops.constructions.utils import update_surface_construction
from replan2eplus.ops.subsurfaces.ezobject import Edge
from replan2eplus.ops.subsurfaces.interfaces import ZoneEdge
from replan2eplus.ops.subsurfaces.logic.select import get_surface_between_zones
from replan2eplus.ops.zones.ezobject import Zone


def update_airboundary_constructions(
    idf: IDF,
    edges: list[Edge],
    zones: list[Zone],
):
    zone_edges = [ZoneEdge(*i) for i in edges if not i.is_directed_edge]
    assert len(edges) == len(zone_edges), (
        f"All airboundary edges need to be between zones! Instead have {edges}"
    )

    const = IDFAirboundaryConstruction()
    const.write(idf)

    airboundaries: list[Airboundary] = []

    for zone_edge, edge in zip(zone_edges, edges):
        main_surface, nb_surface = get_surface_between_zones(zone_edge, zones)
        update_surface_construction(
            idf, main_surface, const.Name, check_constructions=False
        )
        update_surface_construction(
            idf, nb_surface, const.Name, check_constructions=False
        )

        airboundaries.extend(
            [Airboundary(main_surface, edge), Airboundary(nb_surface, edge)]
        )

    return airboundaries
