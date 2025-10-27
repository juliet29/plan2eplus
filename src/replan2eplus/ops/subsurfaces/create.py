from geomeppy import IDF
from utils4plans.lists import chain_flatten

from replan2eplus.ops.surfaces.utils import update_surface_relations
from replan2eplus.ops.subsurfaces.logic.exterior import (
    create_subsurface_for_exterior_edge,
)
from replan2eplus.ops.subsurfaces.logic.interior import (
    create_subsurface_for_interior_edge,
)
from replan2eplus.ops.subsurfaces.user_interfaces import (
   SubsurfaceInputs
)
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.zones.ezobject import Zone
from replan2eplus.ops.subsurfaces.idfobject import IDFSubsurfaceBase, read_subsurfaces
from rich import print


def create_subsurfaces(
    inputs: SubsurfaceInputs| None,
    surfaces: list[Surface],
    zones: list[Zone],
    idf: IDF,
):
    existing_subsurfaces = [i.create_ezobject(surfaces) for i in read_subsurfaces(idf)]

    if inputs:
        interior_subsurfaces = chain_flatten(
            [
                create_subsurface_for_interior_edge(edge, detail, zones, surfaces, idf)
                for edge, detail in inputs.zone_pairs
            ]
        )
        exterior_subsurfaces = [
            create_subsurface_for_exterior_edge(edge, detail, zones, surfaces, idf)
            for edge, detail in inputs.zone_drn_pairs
        ]

        for surf in surfaces:
            # print(f"checking surf: {surf.surface_name}")
            update_surface_relations(idf, surf)

        return interior_subsurfaces + exterior_subsurfaces + existing_subsurfaces

    return existing_subsurfaces
