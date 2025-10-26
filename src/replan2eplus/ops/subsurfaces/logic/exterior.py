from geomeppy import IDF

from replan2eplus.geometry import domain
from replan2eplus.ops.subsurfaces.interfaces import Edge
from replan2eplus.ops.subsurfaces.interfaces import ZoneDirectionEdge
from replan2eplus.ops.subsurfaces.logic.placement import place_domain
from replan2eplus.ops.subsurfaces.logic.prepare import (
    compare_and_maybe_change_dimensions,
    prepare_object,
)
from replan2eplus.ops.subsurfaces.logic.select import (
    get_surface_between_zone_and_direction,
)
from replan2eplus.ops.subsurfaces.user_interfaces import Detail
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.zones.ezobject import Zone


# TODO: needs assurance that the subsurfaces is not orthogonal -> result of get_drn between zone and direction..
def create_subsurface_for_exterior_edge(
    edge: ZoneDirectionEdge,
    detail_: Detail,
    zones: list[Zone],
    surfaces: list[Surface],
    idf: IDF,
):
    surface = get_surface_between_zone_and_direction(edge, zones)

    # TODO check is not air boundary! -> maybe larger check when placing airboundaires to ensure the surface is internal
    assert isinstance(surface.domain, domain.Domain)

    detail = compare_and_maybe_change_dimensions(detail_, surface.domain)
    subsurf_domain = place_domain(surface.domain, *detail.location, detail.dimension)
    obj = prepare_object(
        surface.surface_name, subsurf_domain, surface.domain, detail, "", False
    )
    try:
        obj.write(idf)
    except AttributeError:
        print(obj.values)
        raise Exception("Problem writing Subusrface Object!")
    return obj.create_ezobject(surfaces)
