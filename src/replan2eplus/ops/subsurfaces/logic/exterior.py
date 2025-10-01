from replan2eplus.ezobjects.subsurface import Edge, Subsurface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.ops.subsurfaces.logic.placement import place_domain
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ops.subsurfaces.interfaces import Details, ZoneDirectionEdge
from replan2eplus.ops.subsurfaces.logic.prepare import (
    compare_and_maybe_change_dimensions,
    prepare_object,
)
from replan2eplus.ops.subsurfaces.logic.select import (
    get_surface_between_zone_and_direction,
)
from replan2eplus.idfobjects.subsurface import SubsurfaceKey


def create_subsurface_for_exterior_edge(
    edge: ZoneDirectionEdge, detail_: Details, zones: list[Zone], idf: IDF
):
    key: SubsurfaceKey = detail_.type_.upper()  # type: ignore #TODO verify!

    surface = get_surface_between_zone_and_direction(edge, zones)

    # TODO check is not air boundary! -> maybe larger check when placing airboundaires to ensure the surface is internal

    detail = compare_and_maybe_change_dimensions(detail_, surface.domain)
    subsurf_domain = place_domain(surface.domain, *detail.location, detail.dimension)
    obj = idf.add_subsurface(
        key,
        prepare_object(surface.surface_name, subsurf_domain, surface.domain, detail),
    )
    return Subsurface(obj, key, surface, Edge(edge.space_a, edge.space_b.name))
