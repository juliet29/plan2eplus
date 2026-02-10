from geomeppy import IDF

from plan2eplus.ops.airboundary.ezobject import Airboundary
from plan2eplus.ops.airboundary.idfobject import (
    IDFAirboundaryConstruction,
)
from plan2eplus.ops.constructions.utils import update_surface_construction
from plan2eplus.ops.subsurfaces.interfaces import Edge
from plan2eplus.ops.subsurfaces.interfaces import ZoneEdge
from plan2eplus.ops.subsurfaces.logic.select import get_surface_between_zones
from plan2eplus.ops.surfaces.ezobject import Surface
from plan2eplus.ops.zones.ezobject import Zone


def check_for_existing_airboundaries(idf: IDF, surfaces: list[Surface]):
    existing_airboundary_objects = IDFAirboundaryConstruction.read(idf)
    if not existing_airboundary_objects:
        return []

    airboundary_construction_names = list(map(lambda x: x.Name, existing_airboundary_objects))
    res = map(
        lambda x: Airboundary(x, x.edge),
        filter(
            lambda x: x.construction_name in airboundary_construction_names, surfaces
        ),
    )
    return list(res)


def update_airboundary_constructions(
    idf: IDF, edges: list[Edge], zones: list[Zone], surfaces: list[Surface]
):
    existing_airboundaries = check_for_existing_airboundaries(idf, surfaces)

    if edges:
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

        return airboundaries + existing_airboundaries
    return existing_airboundaries
