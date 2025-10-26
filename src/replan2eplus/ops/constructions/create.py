from pathlib import Path

from geomeppy import IDF

from replan2eplus.ops.constructions.interfaces import EPConstructionSet
from replan2eplus.ops.constructions.logic import (
    update_surfaces_with_construction_set,
)
from replan2eplus.ops.constructions.utils import read_constructions_and_assoc_materials
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.surfaces.ezobject import Surface


def create_constructions(
    idf: IDF,
    const_idf_paths: list[Path],
    mat_idf_paths: list[Path],
    construction_set: EPConstructionSet,
    surfaces: list[Surface],
    subsurfaces: list[Subsurface],
):
    con_mats = read_constructions_and_assoc_materials(
        const_idf_paths, mat_idf_paths, construction_set.names
    )
    con_mats.write(idf)

    update_surfaces_with_construction_set(idf, construction_set, surfaces, subsurfaces)
