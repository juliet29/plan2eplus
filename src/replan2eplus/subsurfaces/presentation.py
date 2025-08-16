from replan2eplus.ezobjects.idf import SubsurfaceObject, SubsurfaceKey, IDF
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.geometry.domain_create import place_domain
from replan2eplus.subsurfaces.interfaces import Details, ZoneEdge, ZoneDirectionEdge
from replan2eplus.subsurfaces.logic import get_surface_between_zones


def create_subsurface_for_interior_edge(
    edge: ZoneEdge, detail: Details, zones: list[Zone], idf: IDF
) -> tuple[Subsurface, Subsurface]:
    def create_ss_name(surface_name:str):
        return f"{detail.type_}__{surface_name}"

    # TODO -> warn if creating a window//
    def create_ss_object(surface_name: str):
        return SubsurfaceObject(
            create_ss_name(surface_name), surface_name, *coords, *dims
        )

    main_surface, nb_surface = get_surface_between_zones(
        edge, zones
    )  # TODO return partner edge also..

    subsurf_domain = place_domain(
        main_surface.domain, *detail.location, detail.dimension
    )
    coords = subsurf_domain.corner.SOUTH_WEST.as_tuple
    dims = detail.dimension.as_tuple

    key: SubsurfaceKey = (f"{detail.type_}:Interzone").upper() # type: ignore

    main_obj = idf.add_subsurface(key, create_ss_object(main_surface.surface_name))
    nb_obj = idf.add_subsurface(key, create_ss_object(nb_surface))

    return Subsurface(main_obj, key), Subsurface(nb_obj, key)


def create_subsurface_for_exterior_edge(
    edge: ZoneDirectionEdge, detail: Details, zones: list[Zone]
):
    pass


def create_subsurfaces(
    edges: list[ZoneEdge | ZoneDirectionEdge],
    details: list[Details],
    edge_detail_map: dict,
    zones: list[Zone],
):
    pass
