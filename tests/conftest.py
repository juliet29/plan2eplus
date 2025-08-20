from replan2eplus.examples.minimal import (
    get_minimal_case,
    get_minimal_idf,
    get_minimal_case_with_rooms,
)
from replan2eplus.examples.existing import get_example_idf
from replan2eplus.examples.subsurfaces import get_minimal_case_with_subsurfaces
import pytest



@pytest.fixture()
def get_pytest_example_idf():  # TODO phase this out?
    return get_example_idf()


@pytest.fixture()
def get_pytest_minimal_idf():  # TODO this could be combined with the next?
    return get_minimal_idf()


@pytest.fixture()
def get_pytest_minimal_case():
    return get_minimal_case()


@pytest.fixture()
def get_pytest_minimal_case_with_rooms():
    return get_minimal_case_with_rooms()


@pytest.fixture()
def get_pytest_minimal_case_with_subsurfaces():
    return get_minimal_case_with_subsurfaces()
