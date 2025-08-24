from pathlib import Path
import pytest
from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.examples.materials import (
    PATH_TO_MATERIALS_IDF,
    PATH_TO_WINDOW_GLASS_IDF,
    PATH_TO_WINDOW_GAS_IDF,
)
from replan2eplus.examples.existing import get_example_idf
from replan2eplus.examples.defaults import PATH_TO_IDD
from replan2eplus.materials.logic import create_materials_from_other_idf
from utils4plans.sets import set_intersection, set_difference


material_groups: list[tuple[Path, list[str]]] = [
    (PATH_TO_MATERIALS_IDF, ["F12 Asphalt shingles", "F13 Built-up roofing"]),
    (PATH_TO_MATERIALS_IDF, ["F12 Asphalt shingles", "F04 Wall air space resistance"]),
    (PATH_TO_WINDOW_GLASS_IDF, ["COATED POLY-33", "ECREF-2 COLORED 6MM"]),
    (PATH_TO_WINDOW_GAS_IDF, ["KRYPTON 3MM", "XENON 13MM"]),
]


@pytest.mark.parametrize("idf, material_names", material_groups)
def test_material_copy_and_convert(idf, material_names):
    material_pairs = create_materials_from_other_idf(
        idf,
        PATH_TO_IDD,
        material_names,
    )
    assert len(material_pairs) == 2


def test_raise_error_for_bad_material():
    with pytest.raises(IDFMisunderstandingError):
        create_materials_from_other_idf(
            PATH_TO_MATERIALS_IDF,
            PATH_TO_IDD,
            ["F12 Asphalt shingles", "My bad material hehe"],
        )


def test_different_material_types_copy_and_convert():
    material_pairs = create_materials_from_other_idf(
        PATH_TO_MATERIALS_IDF,
        PATH_TO_IDD,
        ["F12 Asphalt shingles", "F04 Wall air space resistance"],
    )
    assert len(material_pairs) == 2


def test_adding_material_to_idf(get_pytest_minimal_idf):
    material_names = ["F12 Asphalt shingles", "F04 Wall air space resistance"]
    material_pair = create_materials_from_other_idf(
        PATH_TO_MATERIALS_IDF,
        PATH_TO_IDD,
        material_names,
    )
    idf = get_pytest_minimal_idf

    for mat_pair in material_pair:
        obj0, object_ = idf.add_material(mat_pair.key, mat_pair.object_)

    idf_materials = idf.get_materials()
    assert set([i.Name for i in idf_materials]) == set(material_names)


# @pytest.mark.skip()
# def test_construction_sharing():
#     construction = "random_const"
#     wall_set = WallConstSet(construction)
#     assert wall_set.interior == wall_set.constr
#     assert wall_set.exterior == wall_set.constr

# @pytest.mark.skip()
# def test_construction_partial_sharing():
#     construction = "random_const"
#     construction2 = "rando_cons2"
#     wall_set = WallConstSet(construction, exterior=construction2)
#     assert wall_set.interior == wall_set.constr
#     assert wall_set.exterior == construction2


def test_set_diff():
    # TODO put this test in utils4plans
    la = [123, 456]
    lb = [5, 4, 1, 34, 2, 8, 9, 3]
    assert set_difference(lb, la)


if __name__ == "__main__":
    materials = create_materials_from_other_idf(
        PATH_TO_WINDOW_GAS_IDF,
        PATH_TO_IDD,
        ["KRYPTON 3MM", "XENON 13MM"],
    )
    print(materials[0])

    # test_material_copy_and_convert()
