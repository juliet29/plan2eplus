from utils4plans.sets import set_equality
from utils4plans.lists import chain_flatten

from replan2eplus.ex.main import Cases, ExampleCase, Interfaces

from replan2eplus.idfobjects.base import get_names_of_idf_objects
from replan2eplus.ops.constructions.idfobject import IDFConstruction
from replan2eplus.ops.constructions.utils import (
    read_constructions_by_name_from_many_idfs,
    read_materials_for_construction,
    read_constructions_and_assoc_materials,
)
from replan2eplus.paths import ep_paths
from rich import print


def test_read_constructions():
    case = Cases().example
    constructions = IDFConstruction.read(case.idf)
    const_names = get_names_of_idf_objects(constructions)
    assert set_equality(const_names, ExampleCase.constructions)


def test_read_construction_by_name():
    case = Cases().example
    name = ExampleCase.constructions[0]
    constructions = IDFConstruction.read_by_name(case.idf, [name])
    const_names = get_names_of_idf_objects(constructions)
    assert set_equality(const_names, [name])


def test_read_material_based_on_construction():
    case = Cases().example
    assert case.idf_path
    name = ExampleCase.constructions[0]
    construction = IDFConstruction.read_by_name(
        case.idf, [name]
    )  # TODO special handling if its just one object
    assert len(construction) == 1

    found_materials = read_materials_for_construction([case.idf_path], construction[0])
    assert set_equality(
        get_names_of_idf_objects(found_materials), construction[0].materials
    )


def test_read_construction_across_idfs():
    names = Interfaces.constructions.constructions_across_idfs
    found_constructions = read_constructions_by_name_from_many_idfs(
        ep_paths.construction_paths.constructiin_idfs, names
    )
    print(found_constructions)
    print(chain_flatten([i.materials for i in found_constructions]))
    assert set_equality(get_names_of_idf_objects(found_constructions), names)


def test_read_constructions_and_materials_across_idfs():
    const_names = Interfaces.constructions.constructions_across_idfs
    cpaths = ep_paths.construction_paths
    results = read_constructions_and_assoc_materials(
        cpaths.constructiin_idfs, cpaths.material_idfs, const_names
    )
    result_names = get_names_of_idf_objects(results.constructions + results.materials)
    print(results)
    mat_names = Interfaces.constructions.materials_for_const_across_idfs
    assert set_equality(result_names, mat_names + const_names)


if __name__ == "__main__":
    test_read_constructions_and_materials_across_idfs()
    pass
    # read_material_based_on_construction()
