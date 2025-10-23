from utils4plans.sets import set_equality

from replan2eplus.ex.main import Cases, ExampleCase, Interfaces
from replan2eplus.idfobjects.base import get_names_of_idf_objects
from replan2eplus.ops.constructions.idfobject import IDFConstruction
from replan2eplus.ops.constructions.utils import (
    read_constructions_from_many_idf,
    read_materials_for_construction,
)
from replan2eplus.paths import ep_paths


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
    assert set_equality(get_names_of_idf_objects(found_materials), construction[0].materials)


def test_read_construction_across_idfs():
    names = Interfaces.constructions.constructions_across_idfs
    found_constructions = read_constructions_from_many_idf(
        ep_paths.construction_paths.constructiin_idfs, names
    )
    assert set_equality(get_names_of_idf_objects(found_constructions), names)



if __name__ == "__main__":
    pass
    # read_material_based_on_construction()
