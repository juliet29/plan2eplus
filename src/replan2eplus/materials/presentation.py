from pathlib import Path
from re import L
from typing import Any, NamedTuple
import warnings

from utils4plans.sets import set_difference

from replan2eplus.ezobjects.epbunch_utils import classFromArgs
from replan2eplus.ezobjects.material import Material
import replan2eplus.materials.interfaces as mat_interfaces
from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.ezobjects.epbunch_utils import (
    create_dict_from_fields,
)
from replan2eplus.idfobjects.idf import IDF, EpBunch
from replan2eplus.materials.interfaces import (
    MaterialKey,
    MaterialObjectBase,
    material_keys,
)

# TODO could also call logic?


class MaterialPair(NamedTuple):
    key: MaterialKey
    object_: MaterialObjectBase


def map_materials(key: MaterialKey, values: dict[str, Any]):
    match key:
        case "MATERIAL":
            return mat_interfaces.MaterialObject(**values)

        case "MATERIAL:NOMASS":
            return mat_interfaces.MaterialNoMassObject(**values)

        case "MATERIAL:AIRGAP":
            return mat_interfaces.MaterialAirGap(**values)

        case "WINDOWMATERIAL:GLAZING":  # TODO -> this is not the best, bc what if get more information? Its excluded!
            return classFromArgs(mat_interfaces.WindowMaterialGlazingObject, values)

        case "WINDOWMATERIAL:GAS":
            return classFromArgs(mat_interfaces.WindowMaterialGasObject, values)

        case "_":
            raise NotImplementedError("Don't have an object for this kind of material!")


def get_material_epbunch_key(epbunch: EpBunch) -> MaterialKey:
    val = epbunch.key.upper()
    assert val in material_keys
    return val  # type: ignore --- checked above


# TODO expose as a function that can be called.. 
def create_materials_from_other_idf(
    path_to_idf: Path, path_to_idd: Path, material_names: list[str] = []
):
    """
    default of not specifying any material_names means return all
    """

    def check_material_names():
        differing_names = set_difference(material_names, [i.Name for i in epbunches])
        if (
            set(differing_names) == set(material_names)
        ):  # essentially none of the materials exist in the set -> otherwise we will take what we can
            raise IDFMisunderstandingError(
                f"No materials with names in {differing_names} exist in this IDF!"
            )
        if differing_names:
            warnings.warn(
                f"{differing_names} cannot be found in this IDF `{path_to_idf.parent}`",
                UserWarning,
            )

    other_idf = IDF(path_to_idd, path_to_idf)
    epbunches = other_idf.get_materials()
    check_material_names()

    if material_names:
        epbunches = [i for i in epbunches if i.Name in material_names]

    # TODO could clean this up, but easier to test this way..
    results: list[MaterialPair] = []
    for bunch in epbunches:
        bunch_dict = create_dict_from_fields(bunch)
        key = get_material_epbunch_key(bunch)
        object = map_materials(key, bunch_dict)
        results.append(MaterialPair(key, object))
    return results


# TODO add materials directly (without copying? -> think the below already solves for that.. )

# TODO can avoid need for material pair by adding key to the object itself.. 
def add_materials(idf: IDF, material_pairs: list[MaterialPair]):
    new_materials: list[Material] = []
    for mat_pair in material_pairs:
        (
            epbunch,
            key,
            mat_obj,
        ) = idf.add_material(mat_pair.key, mat_pair.object_)
        new_materials.append(Material(epbunch, key, mat_obj))
    return new_materials
