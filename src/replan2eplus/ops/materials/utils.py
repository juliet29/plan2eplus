from pathlib import Path

from expression.collections import Seq
from geomeppy import IDF
from utils4plans.lists import chain_flatten

from replan2eplus.ezcase.ez import EZ
from replan2eplus.ops.materials.idfobject import IDFMaterialType, material_objects




def read_materials(idf: IDF, names: list[str]):
    k = Seq(material_objects).map(lambda x: x.read(idf, names)).pipe(chain_flatten)
    return k


def read_materials_from_many_idf(idf_paths: list[Path], names: list[str]):
    materials = (
        Seq(idf_paths)
        .map(lambda x: EZ(x).idf)
        .map(lambda x: read_materials(x, names))
        .pipe(chain_flatten)
    )
    # TODO define set? how about uniqueness and duplicate materials?
    return materials


