from geomeppy import IDF
from utils4plans.sets import set_equality
from utils4plans.lists import chain_flatten

from replan2eplus.ex.main import Cases, EpAFNCase, Interfaces

from replan2eplus.idfobjects.base import get_names_of_idf_objects
from replan2eplus.ops.constructions.idfobject import IDFConstruction
from replan2eplus.ops.constructions.utils import (
    read_constructions_by_name_from_many_idfs,
    read_materials_for_construction,
    read_constructions_and_assoc_materials,
)
from replan2eplus.ops.constructions.presentation import create_constructions
from replan2eplus.ops.subsurfaces.create import read_subsurfaces
from replan2eplus.paths import ep_paths
from rich import print
from replan2eplus.ex.materials import SAMPLE_CONSTRUCTION_SET
from replan2eplus.ops.subsurfaces.idfobject import IDFSubsurfaceBase
from replan2eplus.ops.surfaces.idfobject import IDFSurface


def test_read_constructions():
    case = Cases().ep_afn
    constructions = IDFConstruction.read(case.idf)
    const_names = get_names_of_idf_objects(constructions)
    assert set_equality(const_names, EpAFNCase.constructions)


def test_read_construction_by_name():
    case = Cases().ep_afn
    name = EpAFNCase.constructions[0]
    constructions = IDFConstruction.read_by_name(case.idf, [name])
    const_names = get_names_of_idf_objects(constructions)
    assert set_equality(const_names, [name])


def test_read_material_based_on_construction():
    case = Cases().ep_afn
    assert case.idf_path
    name = EpAFNCase.constructions[0]
    construction = IDFConstruction.read_by_name(
        case.idf, [name]
    )  # TODO special handling if its just one object
    assert len(construction) == 1

    found_materials = read_materials_for_construction([case.idf_path], construction[0])
    assert set_equality(
        get_names_of_idf_objects(found_materials), construction[0].materials
    )


def test_read_construction_across_idfs():
    names = Interfaces.constructions.constructions_across_idfs
    found_constructions = read_constructions_by_name_from_many_idfs(
        ep_paths.construction_paths.constructiin_idfs, names
    )
    print(found_constructions)
    print(chain_flatten([i.materials for i in found_constructions]))
    assert set_equality(get_names_of_idf_objects(found_constructions), names)


def test_read_constructions_and_materials_across_idfs():
    const_names = Interfaces.constructions.constructions_across_idfs
    cpaths = ep_paths.construction_paths
    results = read_constructions_and_assoc_materials(
        cpaths.constructiin_idfs, cpaths.material_idfs, const_names
    )
    result_names = get_names_of_idf_objects(results.constructions + results.materials)
    print(results)
    mat_names = Interfaces.constructions.materials_for_const_across_idfs
    assert set_equality(result_names, mat_names + const_names)


def test_write_constructions():
    source_case = Cases().ep_afn
    source_constructions = IDFConstruction.read(source_case.idf)
    destination_case = Cases().base
    new_idf = IDF()
    for constructuon in source_constructions:
        new_idf = constructuon.write(destination_case.idf)
    new_constructions = IDFConstruction.read(new_idf)
    assert set_equality(
        get_names_of_idf_objects(new_constructions),
        get_names_of_idf_objects(source_constructions),
    )


def test_write_ep_construction_set():
    case = Cases().subsurfaces_simple
    cpaths = ep_paths.construction_paths
    create_constructions(
        case.idf,
        cpaths.constructiin_idfs,
        cpaths.material_idfs,
        SAMPLE_CONSTRUCTION_SET,
        case.objects.surfaces,
        case.objects.subsurfaces,
    )
    surface_consts = [i.Construction_Name for i in IDFSurface.read(case.idf)]
    subsurface_consts = [i.Construction_Name for i in read_subsurfaces(case.idf)]
    assert set_equality(
        surface_consts + subsurface_consts, SAMPLE_CONSTRUCTION_SET.names
    )


if __name__ == "__main__":
    pass
    # ['Medium Exterior Wall', 'Medium Roof/Ceiling', 'Medium Partitions', 'Medium Floor']

    # read_material_based_on_construction()
