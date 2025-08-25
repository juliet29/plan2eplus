from replan2eplus.examples.defaults import PATH_TO_IDD, PATH_TO_MINIMAL_IDF
from replan2eplus.examples.minimal import test_rooms
from replan2eplus.ezcase.main import EZCase
from replan2eplus.examples.subsurfaces import zone_edge, test_for_airboundary
from replan2eplus.examples.mat_and_const import (
    PATH_TO_MAT_AND_CONST_IDF,
    PATH_TO_WINDOW_CONST_IDF,
    material_idfs,
    SAMPLE_CONSTRUCTION_SET,
)
from replan2eplus.paths import THROWAWAY_PATH

import pytest


def test_ezcase():
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF)
    case.initialize_idf()
    case.add_zones(test_rooms)

    case.add_airboundaries([zone_edge])
    case.add_subsurfaces(test_for_airboundary.inputs)

    case.add_constructions_from_other_idf(
        [PATH_TO_WINDOW_CONST_IDF, PATH_TO_MAT_AND_CONST_IDF],
        material_idfs,
        SAMPLE_CONSTRUCTION_SET,
    )
    case.add_airflownetwork()
    # this should run without error -> will error if there are any "None" values
    # case.idf.print_idf()
    assert 1
    # return case


if __name__ == "__main__":
    case = test_ezcase()
    # case.idf.idf.run(output_directory=THROWAWAY_PATH)
