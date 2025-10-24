from geomeppy import IDF
from utils4plans.sets import set_equality

from replan2eplus.ex.main import Cases, ExampleCase, Interfaces
from replan2eplus.idfobjects.base import get_names_of_idf_objects
from replan2eplus.ops.materials.idfobject import IDFMaterial
from replan2eplus.ops.materials.utils import (
    read_materials,
    read_materials_from_many_idf,
)
from replan2eplus.paths import ep_paths


def test_read_material_of_type_a_from_idf():
    case = Cases().example  # TODO replace with own example once get materials working
    materials = IDFMaterial.read(case.idf)
    found_material_names = [i.Name for i in materials]
    assert set_equality(found_material_names, ExampleCase.basic_material_names)


def test_read_materials_from_idf_by_name():
    case = Cases().example
    found_materials = read_materials(case.idf, ExampleCase.mixed_subset_materials)
    assert set_equality(
        get_names_of_idf_objects(found_materials), ExampleCase.mixed_subset_materials
    )
    # TODO test reading bad materials -> at least create a log..


def test_read_many_materials_from_many_idfs():
    materials = Interfaces.materials.materials_across_idfs
    found_materials = read_materials_from_many_idf(
        ep_paths.construction_paths.material_idfs, materials
    )
    assert set_equality(get_names_of_idf_objects(found_materials), materials)


def test_write_material():
    source_case = Cases().example
    source_materials = IDFMaterial.read(source_case.idf)
    destination_case = Cases().base
    new_idf = source_materials[0].write(destination_case.idf)
    new_materials = IDFMaterial.read(new_idf)
    assert new_materials[0].Name == source_materials[0].Name


def test_write_materials():
    source_case = Cases().example
    source_materials = IDFMaterial.read(source_case.idf)
    destination_case = Cases().base
    new_idf = IDF()
    for material in source_materials:
        new_idf = material.write(destination_case.idf)
    new_materials = IDFMaterial.read(new_idf)
    assert set_equality(
        get_names_of_idf_objects(new_materials),
        get_names_of_idf_objects(source_materials),
    )


if __name__ == "__main__":
    test_read_materials_from_idf_by_name()
