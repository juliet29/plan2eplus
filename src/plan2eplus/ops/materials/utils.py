from pathlib import Path

from expression.collections import Seq
from geomeppy import IDF
from utils4plans.lists import chain_flatten

from plan2eplus.ezcase.utils import open_idf
from plan2eplus.ops.materials.idfobject import IDFMaterialType, material_objects


def read_materials(idf: IDF, names: list[str]):
    k = Seq(material_objects).map(lambda x: x.read_by_name(idf, names)).pipe(chain_flatten)
    return k


def read_materials_from_many_idf(idf_paths: list[Path], names: list[str]):
    materials = (
        Seq(idf_paths)
        .map(lambda x: open_idf(x))
        .map(lambda x: read_materials(x, names))
        .pipe(chain_flatten)
    )
    # TODO define set? how about uniqueness and duplicate materials?
    return materials
