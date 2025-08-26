import pytest
from replan2eplus.airboundary.presentation import update_airboundary_constructions
from replan2eplus.visuals.transformations import (
    subsurface_to_connection_line,
    calculate_cardinal_domain,
)
from replan2eplus.visuals.base_plot import BasePlot
from replan2eplus.examples.subsurfaces import e0


def test_transform_subsurface_to_connection(get_pytest_minimal_case_with_subsurfaces):
    case = get_pytest_minimal_case_with_subsurfaces
    cardinal_domain = calculate_cardinal_domain(case.zones)
    subsurface_to_connection_line(
        case.subsurfaces[0], case.zones, cardinal_domain.cardinal
    )
    assert 1


def test_transform_airboundary_to_connection(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    airboundaries = update_airboundary_constructions(case.idf, [e0], case.zones)
    cardinal_domain = calculate_cardinal_domain(case.zones)
    subsurface_to_connection_line(
        airboundaries[0], case.zones, cardinal_domain.cardinal
    )
    assert 1
