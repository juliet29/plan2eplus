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


def test_read_material_of_type_a_from_idf():
    case = Cases().example  # TODO replace with own example once get materials working
    materials = IDFMaterial.read(case.idf)
    found_material_names = [i.Name for i in materials]
    case_material_names = ExampleCase.basic_material_names
    assert set_equality(found_material_names, case_material_names)


def test_read_materials_from_idf_by_name():
    case = Cases().example
    found_materials = read_materials(case.idf, ExampleCase.mixed_subset_materials)
    assert set_equality(
        get_material_names(found_materials), ExampleCase.mixed_subset_materials
    )
    # TODO test reading bad materials -> at least create a log..


def test_read_many_materials_from_many_idfs():
    idfs = [i for i in ep_paths.construction_paths.material_idfs]
    materials = Interfaces.materials.materials_across_idfs
    found_materials = read_materials_from_many_idf(idfs, materials)
    assert set_equality(get_material_names(found_materials), materials)




if __name__ == "__main__":
    test_read_materials_from_idf_by_name()
