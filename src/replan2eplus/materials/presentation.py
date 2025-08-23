from pathlib import Path
from replan2eplus.ezobjects.material import Material
from replan2eplus.materials.logic import create_materials_from_other_idf
from replan2eplus.idfobjects.idf import IDF, EpBunch
from replan2eplus.idfobjects.materials import MaterialKey, MaterialObject
from replan2eplus.ezobjects.epbunch_utils import get_epbunch_key

def prepare_object(material: Material):
    return MaterialObject(**material._epbunch)


def create_materials_from_read_idf( path_to_idf: Path, path_to_idd: Path,  idf: IDF, material_names: list[str] = [],):
    materials = create_materials_from_other_idf(path_to_idf, path_to_idd, material_names)

    final_materials = []
    for mat in materials:
        obj = idf.add_material(mat.expected_key, prepare_object(mat))
        final_materials.append(Material(obj, get_epbunch_key(obj))) # type: ignore

    return materials




# TODO these can be merged .. 
def create_material_from_input_object():
    pass