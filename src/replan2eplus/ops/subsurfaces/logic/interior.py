from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.ezobjects.subsurface import Edge, Subsurface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ops.subsurfaces.interfaces import Details, ZoneEdge
from replan2eplus.ops.subsurfaces.logic.prepare import (
    compare_and_maybe_change_dimensions,
    prepare_object,
)
from replan2eplus.ops.subsurfaces.logic.placement import place_domain
from replan2eplus.ops.subsurfaces.logic.select import get_surface_between_zones
from replan2eplus.idfobjects.subsurface import SubsurfaceKey


from rich import print as rprint


def check_for_airboundaries(main_surface, nb_surface):
    if main_surface.is_airboundary or nb_surface.is_airboundary:
        main_name = f"Main: {main_surface.surface_name}"
        nb_name = f"Nb: {nb_surface.surface_name}"
        assert main_surface.is_airboundary and nb_surface.is_airboundary, (
            f"Matching surfaces should be airboundaries!!! \n {main_name}' constr: {main_surface.construction_name}\n {nb_name}' constr: {nb_surface.construction_name}"
        )
        raise IDFMisunderstandingError(
            f"{main_name} and {nb_name} are airboundaries! They cannot have surfaces placed on them! "
        )


def create_subsurface_for_interior_edge(
    edge: ZoneEdge, detail_: Details, zones: list[Zone], idf: IDF
) -> tuple[Subsurface, Subsurface]:
    key: SubsurfaceKey = (f"{detail_.type_}:Interzone").upper()  # type: ignore #TODO verify!

    main_surface, nb_surface = get_surface_between_zones(edge, zones)
    try:
        assert main_surface.domain == nb_surface.domain
    except AssertionError:
        rprint("[red]Neigboring surfaces should have matching domains.")
        rprint("\nMain surface:")
        rprint(main_surface.error_string)
        rprint("\nNeighbor surface:")
        rprint(nb_surface.error_string)
        raise Exception()

    check_for_airboundaries(main_surface, nb_surface)

    # TODO check dimensions!
    detail = compare_and_maybe_change_dimensions(detail_, main_surface.domain)

    subsurf_domain = place_domain(
        main_surface.domain, *detail.location, detail.dimension
    )

    main_obj = idf.add_subsurface(
        key,
        prepare_object(
            main_surface.surface_name,
            subsurf_domain,
            main_surface.domain,
            detail,
            nb_surface_name=nb_surface.surface_name,
        ),
    )
    nb_obj = idf.add_subsurface(
        key,
        prepare_object(
            nb_surface.surface_name,
            subsurf_domain,
            main_surface.domain,
            detail,
            nb_surface_name=main_surface.surface_name,
        ),
    )

    return Subsurface(main_obj, key, main_surface, Edge(*edge)), Subsurface(
        nb_obj, key, nb_surface, Edge(*edge)
    )
