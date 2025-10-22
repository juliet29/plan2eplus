from geomeppy import IDF
from utils4plans.lists import chain_flatten

from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.subsurfaces.logic.exterior import (
    create_subsurface_for_exterior_edge,
)
from replan2eplus.ops.subsurfaces.logic.interior import (
    create_subsurface_for_interior_edge,
)
from replan2eplus.ops.subsurfaces.user_interfaces import (
    SubsurfaceInputs,
)
from replan2eplus.ops.zones.ezobject import Zone


def create_subsurfaces(
    inputs: SubsurfaceInputs,
    zones: list[Zone],
    idf: IDF,
):
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
