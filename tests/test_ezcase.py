import pytest
from rich import print as rprint

from replan2eplus.ex.materials import SAMPLE_CONSTRUCTION_SET
from replan2eplus.examples.cases.minimal import test_rooms
from replan2eplus.examples.mat_and_const import (
    PATH_TO_MAT_AND_CONST_IDF,
    PATH_TO_WINDOW_CONST_IDF,
    material_idfs,
)
from replan2eplus.examples.ortho_domain import create_ortho_case
from replan2eplus.examples.paths import PATH_TO_IDD, PATH_TO_MINIMAL_IDF
from replan2eplus.ex.subsurfaces import e0, subsurface_inputs_dict
from replan2eplus.ezcase.main import EZCase
from replan2eplus.idfobjects.variables import default_variables
from replan2eplus.paths import ORTHO_CASE_RESULTS, PATH_TO_WEATHER_FILE


def run_ortho_case(output_directory):
    case = create_ortho_case()
    case.add_constructions_from_other_idf(
        [PATH_TO_WINDOW_CONST_IDF, PATH_TO_MAT_AND_CONST_IDF],
        material_idfs,
        SAMPLE_CONSTRUCTION_SET,
    )
    case.save_and_run_case(path_=output_directory)
    return case


# TODO this should be moved to examples
def run_simple_ezcase(output_directory):
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(test_rooms)
    case.add_subsurfaces(subsurface_inputs_dict["three_details"])

    case.add_constructions_from_other_idf(
        [PATH_TO_WINDOW_CONST_IDF, PATH_TO_MAT_AND_CONST_IDF],
        material_idfs,
        SAMPLE_CONSTRUCTION_SET,
    )
    case.add_airflownetwork()
    case.idf.add_output_variables(default_variables)  # TODO make wrapper..
    case.save_and_run_case(path_=output_directory)
    return case


def run_airboundary_ezcase(output_directory):
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(test_rooms)

    # TODO should be able to initialize with basic objects, they get transofmed
    case.add_airboundaries(
        [e0]
    )  # TODO: refuse to add airboundaries to surface with subsurfaces
    # TODO -> bring the creation up to this test, so can see complexity assoc. w/ creating it..
    case.add_subsurfaces(subsurface_inputs_dict["airboundary"])

    case.add_constructions_from_other_idf(
        [PATH_TO_WINDOW_CONST_IDF, PATH_TO_MAT_AND_CONST_IDF],
        material_idfs,
        SAMPLE_CONSTRUCTION_SET,
    )
    case.add_airflownetwork()
    rprint(case.airflownetwork)
    case.idf.add_output_variables(default_variables)  # TODO make wrapper..
    case.save_and_run_case(path_=output_directory)
    return case


@pytest.mark.slow
def test_ezcase(tmp_path):
    run_airboundary_ezcase(tmp_path)
    # this should run without error -> will error if there are any "None" values
    # TODO check for None values in IDF.. or at least test inputs..
    # case.idf.print_idf()
    assert 1


# @pytest.mark.slow
def test_ortho_ezcase(tmp_path):
    run_ortho_case(tmp_path)
    # this should run without error -> will error if there are any "None" values
    # TODO check for None values in IDF.. or at least test inputs..
    # case.idf.print_idf()
    assert 1


@pytest.mark.slow
def test_ezcase_simple_subsurfaces(tmp_path):
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(test_rooms)
    case.add_subsurfaces(subsurface_inputs_dict["simple"])

    case.add_constructions_from_other_idf(
        [PATH_TO_WINDOW_CONST_IDF, PATH_TO_MAT_AND_CONST_IDF],
        material_idfs,
        SAMPLE_CONSTRUCTION_SET,
    )
    # case.add_airflownetwork()
    case.save_and_run_case(path_=tmp_path)
    assert 1


if __name__ == "__main__":
    case = run_ortho_case(output_directory=ORTHO_CASE_RESULTS)
    # case = test_ezcase()
    # case.save_and_run_case(path_=THROWAWAY_PATH)
