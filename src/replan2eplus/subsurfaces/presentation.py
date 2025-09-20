from replan2eplus.ezobjects.epbunch_utils import chain_flatten

from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.geometry.range import Range
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ezobjects.subsurface import SubsurfaceOptions, Subsurface, Edge
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.domain_create import Dimension, place_domain
from replan2eplus.idfobjects.subsurface import SubsurfaceKey, SubsurfaceObject
from replan2eplus.subsurfaces.interfaces import (
    Details,
    SubsurfaceInputs,
    ZoneDirectionEdge,
    ZoneEdge,
)
from replan2eplus.subsurfaces.logic import (
    get_surface_between_zone_and_direction,
    get_surface_between_zones,
)
from replan2eplus.subsurfaces.config import DOMAIN_SHRINK_FACTOR
from rich import print as rprint


def compare_and_maybe_change_dimensions(detail: Details, domain: Domain):
    def compare_and_maybe_change_dimension(
        dimension: float, range_: Range, shrink_factor=DOMAIN_SHRINK_FACTOR
    ):
        if dimension >= range_.size:
            return range_.size * shrink_factor
        return dimension

    dimension = detail.dimension
    width = compare_and_maybe_change_dimension(dimension.width, domain.horz_range)
    height = compare_and_maybe_change_dimension(dimension.height, domain.vert_range)
    return Details(Dimension(width, height), detail.location, detail.type_)


def compare_range(range_: Range, subsurf_range_: Range):
    if subsurf_range_.min < range_.min or subsurf_range_.max > range_.max:
        raise Exception(
            f"Arrangement is invalid! Domain range: {range_}. Subsurface range: {subsurf_range_}"
        )  # TODO add more contxt!


def compare_domain(domain: Domain, subsurf_domain: Domain):
    compare_range(domain.horz_range, subsurf_domain.horz_range)
    compare_range(domain.vert_range, subsurf_domain.vert_range)


def create_ss_name(surface_name: str, detail: Details):
    if surface_name:
        return f"{detail.type_}__{surface_name}"
    else:
        return ""


# TODO this goes to logic! TODO number files in logic _04_indiv_subsurf
def prepare_object(
    surface_name: str,
    subsurf_domain: Domain,
    main_surface_domain: Domain,
    detail: Details,
    nb_surface_name: str = "",
):
    # HERE CHECK SUBSURF DOMAINS..
    compare_domain(main_surface_domain, subsurf_domain)

    subsurf_coord = subsurf_domain.corner.SOUTH_WEST
    surf_coord = main_surface_domain.corner.SOUTH_WEST
    coords = (
        subsurf_coord.x - surf_coord.x,
        subsurf_coord.y - surf_coord.y,
    )  # need to subtract the surface corner..
    dims = detail.dimension.as_tuple

    return SubsurfaceObject(
        create_ss_name(surface_name, detail),
        surface_name,
        *coords,
        *dims,
        Outside_Boundary_Condition_Object=create_ss_name(nb_surface_name, detail),
    )


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


def create_subsurface_for_exterior_edge(
    edge: ZoneDirectionEdge, detail_: Details, zones: list[Zone], idf: IDF
):
    key: SubsurfaceOptions = detail_.type_.upper()  # type: ignore #TODO verify!

    surface = get_surface_between_zone_and_direction(edge, zones)

    # TODO check is not air boundary! -> maybe larger check when placing airboundaires to ensure the surface is internal

    # TODO check dimensions!
    detail = compare_and_maybe_change_dimensions(detail_, surface.domain)
    subsurf_domain = place_domain(surface.domain, *detail.location, detail.dimension)
    obj = idf.add_subsurface(
        key,
        prepare_object(surface.surface_name, subsurf_domain, surface.domain, detail),
    )
    return Subsurface(obj, key, surface, Edge(edge.space_a, edge.space_b.name))


# TODO this should be dealing w/ different APIs..
def create_subsurfaces(
    inputs: SubsurfaceInputs,
    zones: list[Zone],
    idf: IDF,
):
    # TODO fix chain_flatten in utils4plans to use typevar
    interior_subsurfaces: list[Subsurface] = chain_flatten(
        [
            create_subsurface_for_interior_edge(edge, detail, zones, idf)
            for edge, detail in inputs.zone_pairs
        ]
    )
    exterior_subsurfaces = [
        create_subsurface_for_exterior_edge(edge, detail, zones, idf)
        for edge, detail in inputs.zone_drn_pairs
    ]

    return interior_subsurfaces + exterior_subsurfaces
