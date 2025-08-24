from replan2eplus.airboundary.interfaces import AirboundaryConstructionObject
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.subsurfaces.interfaces import ZoneEdge
from replan2eplus.subsurfaces.logic import get_surface_between_zones


def add_airboundary_construction(idf: IDF, object_: AirboundaryConstructionObject):
    idf.add_airboundary_construction(object_)


def update_airboundary_constructions(
    idf: IDF,
    edges: list[ZoneEdge],
    zones: list[Zone],
):
    airboundary_object = AirboundaryConstructionObject("Default Airboundary")
    add_airboundary_construction(idf, airboundary_object)

    changed_surfaces: list[Surface] = []

    for edge in edges:
        main_surface, nb_surface = get_surface_between_zones(edge, zones)
        idf.update_construction(main_surface, airboundary_object.Name)
        idf.update_construction(nb_surface, airboundary_object.Name)

        changed_surfaces.extend([main_surface, nb_surface])

    return changed_surfaces
