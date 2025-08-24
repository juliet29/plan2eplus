from replan2eplus.airboundary.interfaces import (
    DEFAULT_AIRBOUNDARY_OBJECT,
    AirboundaryConstructionObject,
)
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.subsurfaces.interfaces import ZoneEdge
from replan2eplus.subsurfaces.logic import get_surface_between_zones
from replan2eplus.ezobjects.airboundary import Airboundary


def add_airboundary_construction(idf: IDF, object_: AirboundaryConstructionObject):
    idf.add_airboundary_construction(object_)


def update_airboundary_constructions(
    idf: IDF,
    edges: list[ZoneEdge],
    zones: list[Zone],
):
    add_airboundary_construction(idf, DEFAULT_AIRBOUNDARY_OBJECT)

    airboundaries: list[Airboundary] = []

    for edge in edges:
        main_surface, nb_surface = get_surface_between_zones(edge, zones)
        idf.update_construction(main_surface, DEFAULT_AIRBOUNDARY_OBJECT.Name)
        idf.update_construction(nb_surface, DEFAULT_AIRBOUNDARY_OBJECT.Name)

        airboundaries.extend(
            [Airboundary(main_surface, edge), Airboundary(nb_surface, edge)]
        )

    return airboundaries
