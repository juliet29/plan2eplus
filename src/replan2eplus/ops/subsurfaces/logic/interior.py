from geomeppy import IDF
from rich import print

from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.geometry.domain import Domain
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.subsurfaces.interfaces import ZoneEdge
from replan2eplus.ops.subsurfaces.logic.placement import place_domain
from replan2eplus.ops.subsurfaces.logic.prepare import (
    compare_and_maybe_change_dimensions,
    prepare_object,
)
from replan2eplus.ops.subsurfaces.logic.select import get_surface_between_zones
from replan2eplus.ops.subsurfaces.user_interfaces import Detail
from replan2eplus.ops.zones.ezobject import Zone
from replan2eplus.ops.surfaces.ezobject import Surface


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
    edge: ZoneEdge,
    detail_: Detail,
    zones: list[Zone],
    surfaces: list[Surface],
    idf: IDF,
) -> tuple[Subsurface, Subsurface]:
    main_surface, nb_surface = get_surface_between_zones(edge, zones)
    try:
        assert main_surface.domain == nb_surface.domain
    except AssertionError:
        # TODO make an error class to clean this up
        print("[red]Neigboring surfaces should have matching domains.")
        print("\nMain surface:")
        print(main_surface)
        print("\nNeighbor surface:")
        print(nb_surface)
        raise Exception()

    check_for_airboundaries(main_surface, nb_surface)

    assert isinstance(main_surface.domain, Domain)

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

    # main_obj.write(idf)
    try:
        main_obj.write(idf)
    except AttributeError:
        print(main_obj.values)
        raise Exception("Problem writing Subusrface Object!")

    try:
        nb_obj.write(idf)
    except AttributeError:
        print(nb_obj.values)
        raise Exception("Problem writing Subusrface Object!")

    # nb_obj.write(idf)

    ez_surf_main = main_obj.create_ezobject(surfaces)
    ez_surf_nb = nb_obj.create_ezobject(surfaces)

    return ez_surf_main, ez_surf_nb
