from pathlib import Path
from typing import NamedTuple

from expression.collections import Seq
from geomeppyupdated import IDF
from utils4plans.lists import chain_flatten

from plan2eplus.errors import IDFMisunderstandingError
from plan2eplus.ezcase.utils import open_idf
from plan2eplus.ops.base import get_names_of_idf_objects
from plan2eplus.ops.constructions.idfobject import IDFConstruction
from plan2eplus.ops.materials.idfobject import IDFMaterialType
from plan2eplus.ops.materials.utils import read_materials_from_many_idf
from plan2eplus.ops.subsurfaces.ezobject import Subsurface
from plan2eplus.ops.subsurfaces.idfobject import update_subsurface
from plan2eplus.ops.surfaces.ezobject import Surface
from plan2eplus.ops.surfaces.idfobject import IDFSurface


# TODO move to interfaces.., and move epcosnt to user interfaces
class ConstructionsAndAssocMaterials(NamedTuple):
    constructions: list[IDFConstruction]
    materials: list[IDFMaterialType]  # pyright: ignore[reportGeneralTypeIssues]

    def write_constructions(self, idf: IDF):
        for const in self.constructions:
            idf = const.write(idf)

    def write_materials(self, idf: IDF):
        for mat in self.materials:
            idf = mat.write(idf)

    def write(self, idf: IDF):
        self.write_constructions(idf)
        self.write_materials(idf)


def read_materials_for_construction(
    idf_paths: list[Path],
    construction: IDFConstruction,
):
    materials = read_materials_from_many_idf(idf_paths, construction.materials)
    return materials


def read_constructions_by_name_from_many_idfs(idf_paths: list[Path], names: list[str]):
    constructions = (
        Seq(idf_paths)
        .map(lambda x: open_idf(x))
        .map(lambda x: IDFConstruction.read_by_name(x, names))
        .pipe(chain_flatten)
    )
    # TODO define set? how about uniqueness and duplicate materials?
    return constructions


def read_constructions_and_assoc_materials(
    const_idf_paths: list[Path], mat_idf_paths: list[Path], names: list[str]
):
    constructions = read_constructions_by_name_from_many_idfs(const_idf_paths, names)
    mats_to_find = list(set(chain_flatten([i.materials for i in constructions])))
    materials = read_materials_from_many_idf(mat_idf_paths, mats_to_find)
    return ConstructionsAndAssocMaterials(constructions, materials)


def check_construction_names(idf: IDF, construction_name: str):
    const_names = get_names_of_idf_objects(IDFConstruction.read(idf))
    try:
        assert construction_name in const_names
    except AssertionError:
        raise IDFMisunderstandingError(
            f"`{construction_name}` has not been added to this IDF. The constructions existing are: {const_names}"
        )


def update_surface_construction(
    idf: IDF, surface: Surface, construction_name: str, check_constructions=True
):
    if check_constructions:
        check_construction_names(idf, construction_name)
    IDFSurface().update(
        idf, surface.surface_name, "Construction_Name", construction_name
    )
    surface.construction_name = construction_name


def update_subsurface_construction(
    idf: IDF, surface: Subsurface, construction_name: str
):
    check_construction_names(idf, construction_name)
    update_subsurface(
        idf, surface.subsurface_name, "Construction_Name", construction_name
    )
    surface.construction_name = construction_name
