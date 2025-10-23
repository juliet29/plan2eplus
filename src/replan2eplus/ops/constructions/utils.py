from expression.collections import Seq
from utils4plans.lists import chain_flatten
from pathlib import Path
from replan2eplus.ops.constructions.idfobject import IDFConstruction
from replan2eplus.ezcase.ez import EZ
from replan2eplus.ops.materials.idfobject import IDFMaterialType, material_objects
from replan2eplus.ops.materials.utils import read_materials_from_many_idf


def get_construction_names(constructions: list[IDFConstruction]):
    return [i.Name for i in constructions]


def read_materials_for_construction(
    idf_paths: list[Path],
    construction: IDFConstruction,
):
    materials = read_materials_from_many_idf(idf_paths, construction.materials)
    return materials


def read_constructions_from_many_idf(idf_paths: list[Path], names: list[str]):
    constructions = (
        Seq(idf_paths)
        .map(lambda x: EZ(x).idf)
        .map(lambda x: IDFConstruction.read_by_name(x, names))
        .pipe(chain_flatten)
    )
    # TODO define set? how about uniqueness and duplicate materials?
    return constructions
