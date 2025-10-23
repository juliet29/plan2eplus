from typing import Callable, Iterable
from expression.collections import Seq, seq
from geomeppy import IDF
from utils4plans.lists import chain_flatten_seq
from expression import pipe

from replan2eplus.ops.materials.idfobject import IDFMaterialType, material_objects
from itertools import chain


from typing import TypeVar

T = TypeVar("T")


# def chain_flatten_seq(lst: Iterable[Iterable[T]]):
#     return Seq(list(chain.from_iterable(lst)))


def read_materials(idf: IDF, names: list[str]):
    k = pipe(
        Seq(material_objects).map(lambda x: x.read(idf)),
        chain_flatten_seq,
    ).filter(lambda x: x.Name in names)
    return list(k)


def get_material_names(materials: list[IDFMaterialType]):
    return [i.Name for i in materials]
