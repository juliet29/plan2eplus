from utils4plans.lists import chain_flatten

from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ezobjects.subsurface import SubsurfaceOptions, Subsurface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.idfobjects.subsurface import SubsurfaceKey
from replan2eplus.ops.subsurfaces.interfaces import (
    SubsurfaceInputs,
)
from replan2eplus.ops.subsurfaces.logic.exterior import (
    create_subsurface_for_exterior_edge,
)
from replan2eplus.ops.subsurfaces.logic.interior import (
    create_subsurface_for_interior_edge,
)


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
