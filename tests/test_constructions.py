from replan2eplus.ex.main import Cases, Interfaces, ExampleCase
from replan2eplus.ops.materials.idfobject import IDFMaterial
from utils4plans.sets import set_equality
from replan2eplus.paths import ep_paths
from rich import print
from replan2eplus.ops.materials.utils import (
    read_materials,
    get_material_names,
    read_materials_from_many_idf,
)


def read_material_based_on_construction():
    case = Cases().example
    construction = []
    found_materials = read_materials_for_constructions(case.idf, construction)
    assert set_equality(get_material_names(found_materials), construction)


def read_material_from_many_idfs_based_on_construction():
    idfs = [i for i in ep_paths.construction_paths.material_idfs]
    construction = []
    found_materials = read_materials_for_constructions(idfs, construction)
    assert set_equality(get_material_names(found_materials), construction)


def read_material_from_many_idfs_based_on_many_constructions():
    idfs = [i for i in ep_paths.construction_paths.material_idfs]
    constructions = []
    found_materials = read_materials_for_constructions(idfs, constructions)
    assert set_equality([i.Name for i in found_materials], constructions)
