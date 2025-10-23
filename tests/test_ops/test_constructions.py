from unittest.mock import Base
from replan2eplus.ops.constructions.idfobject import IDFConstruction
from replan2eplus.ops.constructions.logic.update import (
    update_surfaces_with_construction_set,
)
from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.examples.mat_and_const import (
    PATH_TO_MAT_AND_CONST_IDF,
    PATH_TO_WINDOW_GLASS_IDF,
    PATH_TO_WINDOW_CONST_IDF,
    TEST_CONSTRUCTIONS_WITH_WINDOW,
)
from replan2eplus.examples.paths import PATH_TO_IDD
from replan2eplus.ops.constructions.presentation import (
    create_constructions_from_other_idfs,
    add_constructions,
    find_and_add_materials,
)
import pytest
from replan2eplus.examples.mat_and_const import BAD_CONSTRUCTION_SET
from replan2eplus.examples.mat_and_const import CONST_IN_EXAMPLE
from replan2eplus.examples.mat_and_const import TEST_CONSTRUCTIONS


@pytest.fixture()
def get_constructions_from_idf() -> list[IDFConstruction]:
    return create_constructions_from_other_idfs(
        [PATH_TO_MAT_AND_CONST_IDF], PATH_TO_IDD, TEST_CONSTRUCTIONS
    )


def test_get_constructions():
    constructions = create_constructions_from_other_idfs(
        [PATH_TO_MAT_AND_CONST_IDF], PATH_TO_IDD, TEST_CONSTRUCTIONS
    )
    const_names = [i.Name for i in constructions]
    assert set(const_names) == set(TEST_CONSTRUCTIONS)


def test_get_constructions_from_many_idf():
    constructions = create_constructions_from_other_idfs(
        [PATH_TO_MAT_AND_CONST_IDF, PATH_TO_WINDOW_CONST_IDF],
        PATH_TO_IDD,
        TEST_CONSTRUCTIONS_WITH_WINDOW,
    )
    const_names = [i.Name for i in constructions]
    assert set(const_names) == set(TEST_CONSTRUCTIONS_WITH_WINDOW)


def test_add_constructions_without_mats(
    get_pytest_minimal_idf, get_constructions_from_idf
):
    idf = get_pytest_minimal_idf
    constructions_to_add = get_constructions_from_idf
    with pytest.raises(IDFMisunderstandingError):
        add_constructions(idf, constructions_to_add)


def test_find_and_add_materials(get_pytest_minimal_idf, get_constructions_from_idf):
    idf = get_pytest_minimal_idf
    constructions_to_add = get_constructions_from_idf
    new_materials = find_and_add_materials(
        idf,
        constructions_to_add,
        path_to_material_idfs=[PATH_TO_MAT_AND_CONST_IDF, PATH_TO_WINDOW_GLASS_IDF],
        path_to_idd=PATH_TO_IDD,
    )
    assert len(new_materials) == 7
    assert "F08 Metal surface" in [i._idf_name for i in new_materials]


def test_add_constructions_after_materials(
    get_pytest_minimal_idf, get_constructions_from_idf
):
    idf = get_pytest_minimal_idf
    constructions_to_add = get_constructions_from_idf
    new_materials = find_and_add_materials(
        idf,
        constructions_to_add,
        path_to_material_idfs=[PATH_TO_MAT_AND_CONST_IDF],
        path_to_idd=PATH_TO_IDD,
    )
    add_constructions(idf, constructions_to_add)


def test_update_surface_construction(get_pytest_example_case):
    case = get_pytest_example_case
    surf = case.surfaces[0]
    case.idf.update_construction(surf, CONST_IN_EXAMPLE)
    assert surf.construction_name == CONST_IN_EXAMPLE
    idf_surf = [i for i in case.idf.get_surfaces() if i.Name == surf._idf_name][0]
    assert idf_surf.Construction_Name == CONST_IN_EXAMPLE


def test_update_with_construction_set(get_pytest_example_case):
    case = get_pytest_example_case
    update_surfaces_with_construction_set(
        case.idf, BAD_CONSTRUCTION_SET, case.surfaces, case.subsurfaces
    )
    outdoor_walls = [
        i
        for i in case.surfaces
        if i.boundary_condition == "outdoors" and i.type_ == "wall"
    ]
    ground_floors = [
        i
        for i in case.surfaces
        if i.type_ == "floor" and i.boundary_condition == "ground"
    ]
    for i in outdoor_walls:
        assert i.construction_name == "Medium Roof/Ceiling"
    for i in ground_floors:
        assert i.construction_name == "Medium Furnishings"


if __name__ == "__main__":
    test_get_constructions()
