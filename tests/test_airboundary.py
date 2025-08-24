import pytest
from replan2eplus.examples.subsurfaces import zone_edge
from replan2eplus.airboundary.presentation import update_airboundary_constructions


def test_add_airboundary(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    changed_surfaces = update_airboundary_constructions(
        case.idf, [zone_edge], case.zones
    )
    for surf in changed_surfaces:
        assert "Airboundary" in surf.construction_name
