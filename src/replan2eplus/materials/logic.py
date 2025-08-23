from pathlib import Path
from replan2eplus.ezobjects.construction import Construction
from replan2eplus.ezobjects.epbunch_utils import get_epbunch_key
from replan2eplus.ezobjects.material import Material
from replan2eplus.idfobjects.idf import IDF, EpBunch
from replan2eplus.idfobjects.materials import MaterialKey, material_keys, MaterialObject
from typing import NamedTuple

# TODO could also call logic?


class MaterialAndKey(NamedTuple):
    epbunch: EpBunch
    key: str


def create_materials_from_other_idf(
    path_to_idf: Path, path_to_idd: Path, material_names: list[str] = []
):
    """
    default of not specifying any material names means return all
    """
    other_idf = IDF(path_to_idd, path_to_idf)
    material_epbunches = [
        MaterialAndKey(i, get_epbunch_key(i)) for i in other_idf.get_materials()
    ]
    
    # TODO: instead of materials, just get the properties needed to create an epobject. 
    if not material_names:
        return [
            Material(_epbunch=i.epbunch, expected_key=i.key) for i in material_epbunches # type: ignore -> will be correct type -> idf.get_materials() filters 
        ]

    return [
        Material(_epbunch=i.epbunch, expected_key=i.key) for i in material_epbunches # type: ignore
    ]


def create_constructions_from_other_idf(
    path_to_idf: Path, path_to_idd: Path, construction_names: list[str] = []
):
    other_idf = IDF(path_to_idd, path_to_idf)
    construction_epbunches = other_idf.get_materials()
    if not construction_names:
        return [Construction(i, get_epbunch_key(i)) for i in construction_epbunches]

    return [
        Construction(i, get_epbunch_key(i))
        for i in construction_epbunches
        if i.Name in construction_names
    ]
