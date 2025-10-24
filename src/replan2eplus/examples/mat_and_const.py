from pathlib import Path
from replan2eplus.ex.materials import SAMPLE_CONSTRUCTION_SET
from replan2eplus.paths import static_paths
from replan2eplus.ezobjects.construction import EPConstructionSet, BaseConstructionSet
from replan2eplus.ezcase.main import EZCase
from replan2eplus.examples.paths import PATH_TO_IDD, PATH_TO_MINIMAL_IDF
from replan2eplus.paths import PATH_TO_WEATHER_FILE
from replan2eplus.examples.cases.minimal import test_rooms

PATH_TO_MAT_AND_CONST_IDF = (
    static_paths.inputs / "constructions/ASHRAE_2005_HOF_Materials.idf"
)

PATH_TO_WINDOW_CONST_IDF = static_paths.inputs / "constructions/WindowConstructs.idf"

PATH_TO_WINDOW_GLASS_IDF = (
    static_paths.inputs / "constructions/WindowGlassMaterials.idf"
)
PATH_TO_WINDOW_GAS_IDF = static_paths.inputs / "constructions/WindowGasMaterials.idf"

material_idfs = [
    PATH_TO_MAT_AND_CONST_IDF,
    PATH_TO_WINDOW_GLASS_IDF,
    PATH_TO_WINDOW_GAS_IDF,
]
construction_idfs = [PATH_TO_MAT_AND_CONST_IDF, PATH_TO_WINDOW_CONST_IDF]


CONST_IN_EXAMPLE = "Medium Exterior Wall"
TEST_CONSTRUCTIONS = ["Light Exterior Wall", "Light Roof/Ceiling"]
TEST_CONSTRUCTIONS_WITH_WINDOW = [
    "Light Exterior Wall",
    "Light Roof/Ceiling",
    "Sgl Clr 6mm",
]


BAD_CONSTRUCTION_SET = EPConstructionSet(
    wall=BaseConstructionSet("Medium Roof/Ceiling", "Medium Roof/Ceiling"),
    floor=BaseConstructionSet("Medium Partitions", "Medium Furnishings"),
    roof=BaseConstructionSet("Medium Furnishings", "Medium Furnishings"),
    window=BaseConstructionSet("Sgl Clr 6mm", "Sgl Clr 6mm"),
    door=BaseConstructionSet("Medium Partitions", "Medium Partitions"),
)


def get_minimal_case_with_materials():
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(test_rooms)
    case.add_constructions_from_other_idf(
        construction_idfs, material_idfs, SAMPLE_CONSTRUCTION_SET
    )
    return case
