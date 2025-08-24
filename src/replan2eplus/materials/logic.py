from pathlib import Path
from tkinter.dialog import DIALOG_ICON
from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.ezobjects.construction import Construction
from replan2eplus.ezobjects.epbunch_utils import (
    get_epbunch_key,
    create_dict_from_fields,
)
from replan2eplus.ezobjects.material import Material
from replan2eplus.idfobjects.idf import IDF, EpBunch
from replan2eplus.idfobjects.materials import MaterialKey, material_keys
from typing import Any, NamedTuple
from dataclasses import fields
import replan2eplus.materials.interfaces as mat_interfaces
from replan2eplus.materials.interfaces import MaterialObjectBase
from utils4plans.sets import set_difference

# TODO could also call logic?


class MaterialPair(NamedTuple):
    key: MaterialKey
    object_: MaterialObjectBase


def classFromArgs(className, argDict):
    fieldSet = {f.name for f in fields(className) if f.init}
    filteredArgDict = {k: v for k, v in argDict.items() if k in fieldSet}
    return className(**filteredArgDict)


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
    return val  # type: ignore checked above


def create_materials_from_other_idf(
    path_to_idf: Path, path_to_idd: Path, material_names: list[str] = []
):
    """
    default of not specifying any material_names means return all
    """

    def check_material_names():
        differing_names = set_difference(material_names, [i.Name for i in epbunches])
        if differing_names:
            raise IDFMisunderstandingError(
                f"No materials with names in {differing_names} exist in this IDF!"
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
        results.append(MaterialPair(key,  object))
    return results


# def create_constructions_from_other_idf(
#     path_to_idf: Path, path_to_idd: Path, construction_names: list[str] = []
# ):
#     # TODO check that materials of the constructions are in the idf!
#     other_idf = IDF(path_to_idd, path_to_idf)
#     construction_epbunches = other_idf.get_materials()
#     if not construction_names:
#         return [Construction(i, get_epbunch_key(i)) for i in construction_epbunches]

#     return [
#         Construction(i, get_epbunch_key(i))
#         for i in construction_epbunches
#         if i.Name in construction_names
#     ]
