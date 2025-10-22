from geomeppy import IDF
from rich import print as rprint

from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.ops.subsurfaces.ezobject import Edge, Subsurface
from replan2eplus.ops.subsurfaces.interfaces import ZoneEdge
from replan2eplus.ops.subsurfaces.logic.placement import place_domain
from replan2eplus.ops.subsurfaces.logic.prepare import (
    compare_and_maybe_change_dimensions,
    prepare_object,
)
from replan2eplus.ops.subsurfaces.logic.select import get_surface_between_zones
from replan2eplus.ops.subsurfaces.user_interfaces import Detail
from replan2eplus.ops.zones.ezobject import Zone


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
    edge: ZoneEdge, detail_: Detail, zones: list[Zone], idf: IDF
) -> tuple[Subsurface, Subsurface]:

    main_surface, nb_surface = get_surface_between_zones(edge, zones)
    try:
        assert main_surface.domain == nb_surface.domain
    except AssertionError:
        # TODO make an error class to clean this up 
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

    main_obj = prepare_object(
            main_surface.surface_name,
            subsurf_domain,
            main_surface.domain,
            detail,
            nb_surface.surface_name,
            True,
        )
    nb_obj = prepare_object(
        nb_surface.surface_name,
        subsurf_domain,
        main_surface.domain,
        detail,
        main_surface.surface_name,
        True,
    )

    main_obj.write(idf)
    nb_obj.write(idf)

    ez_edge = Edge(*edge)
    ez_surf_main = main_obj.create_ezobject(main_surface, ez_edge)
    ez_surf_nb = nb_obj.create_ezobject(nb_surface, ez_edge)


    return ez_surf_main, ez_surf_nb
