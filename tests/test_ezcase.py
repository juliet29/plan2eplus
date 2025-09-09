from replan2eplus.examples.defaults import PATH_TO_IDD, PATH_TO_MINIMAL_IDF
from replan2eplus.examples.minimal import test_rooms
from replan2eplus.ezcase.main import EZCase
from replan2eplus.examples.subsurfaces import e0, airboundary_subsurface_inputs
from replan2eplus.examples.mat_and_const import (
    PATH_TO_MAT_AND_CONST_IDF,
    PATH_TO_WINDOW_CONST_IDF,
    material_idfs,
    SAMPLE_CONSTRUCTION_SET,
)
from replan2eplus.paths import THROWAWAY_PATH
from replan2eplus.paths import PATH_TO_WEATHER_FILE

import pytest


def test_ezcase():
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(test_rooms)

    # TODO should be able to initialize with basic objects, they get transofmed
    case.add_airboundaries(
        [e0]
    )  # TODO: refuse to add airboundaries to surface with subsurfaces
    # TODO -> bring the creation up to this test, so can see complexity assoc. w/ creating it..
    case.add_subsurfaces(airboundary_subsurface_inputs.inputs)

    case.add_constructions_from_other_idf(
        [PATH_TO_WINDOW_CONST_IDF, PATH_TO_MAT_AND_CONST_IDF],
        material_idfs,
        SAMPLE_CONSTRUCTION_SET,
    )
    case.add_airflownetwork()
    # this should run without error -> will error if there are any "None" values
    # TODO check for None values in IDF.. or at least test inputs..
    # case.idf.print_idf()
    assert 1
    # return case


if __name__ == "__main__":
    case = test_ezcase()
    # case.idf.idf.run(output_directory=THROWAWAY_PATH)
