from pathlib import Path
from utils4plans.sets import set_difference
from replan2eplus.ezobjects.epbunch_utils import create_dict_from_fields
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.constructions.interfaces import ConstructionsObject
import replan2eplus.epnames.keys as epkeys
from replan2eplus.ezobjects.construction import Construction

from replan2eplus.errors import IDFMisunderstandingError
from utils4plans.lists import chain_flatten

from replan2eplus.materials.presentation import (
    MaterialPair,
    create_materials_from_other_idf,
    add_materials,
)


def create_constructions_from_other_idf(
    path_to_idf: Path, path_to_idd: Path, construction_names: list[str] = []
):
    def check_construction_names():
        differing_names = set_difference(
            construction_names, [i.Name for i in epbunches]
        )
        if differing_names:
            raise IDFMisunderstandingError(
                f"No materials with names in {differing_names} exist in this IDF!"
            )

    other_idf = IDF(path_to_idd, path_to_idf)
    epbunches = other_idf.get_constructions()
    check_construction_names()

    if construction_names:
        epbunches = [i for i in epbunches if i.Name in construction_names]

    constructions = [
        ConstructionsObject(**create_dict_from_fields(i)) for i in epbunches
    ]

    return constructions


def check_materials_are_in_idf(const_object: ConstructionsObject, idf: IDF):
    idf_mats = idf.get_materials()
    idf_mat_names = [i.Name for i in idf_mats]
    for mat in const_object.materials:
        try:
            assert (
                mat in idf_mat_names
            )  # TODO: need try-except for assertion! have made this mistake elsewhere -> look for it and fix it!
        except AssertionError:
            raise IDFMisunderstandingError(
                f"`{mat}` needed for this construction is not in IDF materials: {sorted(idf_mat_names)}"
            )


def find_and_add_materials(
    idf: IDF,
    construction_objects: list[ConstructionsObject],
    idf_paths_to_try: list[Path],
    path_to_idd: Path,
):
    materials_to_find: list[str] = chain_flatten(
        [i.materials for i in construction_objects]
    )
    all_mat_pairs: list[MaterialPair] = []
    for path in idf_paths_to_try:
        try:
            mat_pairs = create_materials_from_other_idf(
                path, path_to_idd, materials_to_find
            )
            if mat_pairs:
                all_mat_pairs.extend(mat_pairs)
        except IDFMisunderstandingError:
            pass  # possible that IDF will have NONE of the materials to be foynd

    updated_idf, new_materials = add_materials(idf, all_mat_pairs)
    return updated_idf, new_materials


# TODO: when adding constructions to idf, fail if the constituent materials are not in the new idf..
def add_constructions(idf: IDF, construction_objects: list[ConstructionsObject]):
    results = []
    for const_object in construction_objects:
        check_materials_are_in_idf(const_object, idf)
        new_obj = idf.add_construction(const_object)
        results.append(Construction(new_obj))

    return results
