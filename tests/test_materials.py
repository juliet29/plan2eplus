from pathlib import Path
import pytest
from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.examples.mat_and_const import (
    PATH_TO_MAT_AND_CONST_IDF,
    PATH_TO_WINDOW_GLASS_IDF,
    PATH_TO_WINDOW_GAS_IDF,
)
from replan2eplus.examples.existing import get_example_idf
from replan2eplus.examples.defaults import PATH_TO_IDD
from replan2eplus.ops.materials.presentation import (
    add_materials,
    create_materials_from_other_idfs,
)
from utils4plans.sets import set_intersection, set_difference


material_groups: list[tuple[Path, list[str]]] = [
    (PATH_TO_MAT_AND_CONST_IDF, ["F12 Asphalt shingles", "F13 Built-up roofing"]),
    (
        PATH_TO_MAT_AND_CONST_IDF,
        ["F12 Asphalt shingles", "F04 Wall air space resistance"],
    ),
    (PATH_TO_WINDOW_GLASS_IDF, ["COATED POLY-33", "ECREF-2 COLORED 6MM"]),
    (PATH_TO_WINDOW_GAS_IDF, ["KRYPTON 3MM", "XENON 13MM"]),
]


@pytest.mark.parametrize("idf, material_names", material_groups)
def test_material_copy_and_convert(idf, material_names):
    material_pairs = create_materials_from_other_idfs(
        [idf],
        PATH_TO_IDD,
        material_names,
    )
    assert len(material_pairs) == 2


def test_warns_for_bad_material():
    with pytest.warns(UserWarning):
        create_materials_from_other_idfs(
            [PATH_TO_MAT_AND_CONST_IDF],
            PATH_TO_IDD,
            ["My bad material hehe"],
        )


def test_succeeds_if_at_least_one_good_mat():
    with pytest.warns(UserWarning):
        material_pairs = create_materials_from_other_idfs(
            [PATH_TO_MAT_AND_CONST_IDF],
            PATH_TO_IDD,
            [
                "My bad material hehe",
                "F12 Asphalt shingles",
                "F04 Wall air space resistance",
            ],
        )
        assert len(material_pairs) == 2


def test_different_material_types_copy_and_convert():
    material_pairs = create_materials_from_other_idfs(
        [PATH_TO_MAT_AND_CONST_IDF],
        PATH_TO_IDD,
        ["F12 Asphalt shingles", "F04 Wall air space resistance"],
    )
    assert len(material_pairs) == 2


def test_adding_material_to_idf(get_pytest_minimal_idf):
    material_names = ["F12 Asphalt shingles", "F04 Wall air space resistance"]
    material_pairs = create_materials_from_other_idfs(
        [PATH_TO_MAT_AND_CONST_IDF],
        PATH_TO_IDD,
        material_names,
    )
    idf = get_pytest_minimal_idf

    add_materials(idf, material_pairs)

    idf_materials = idf.get_materials()
    assert set([i.Name for i in idf_materials]) == set(material_names)


def test_set_diff():
    # TODO put this test in utils4plans
    la = [123, 456]
    lb = [5, 4, 1, 34, 2, 8, 9, 3]
    assert set_difference(lb, la)


if __name__ == "__main__":
    materials = create_materials_from_other_idfs(
        [PATH_TO_WINDOW_GAS_IDF],
        PATH_TO_IDD,
        ["KRYPTON 3MM", "XENON 13MM"],
    )
    print(materials[0])

    # test_material_copy_and_convert()
