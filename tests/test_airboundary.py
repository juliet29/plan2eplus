import pytest
from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.examples.subsurfaces import e0, zone_edge
from replan2eplus.airboundary.presentation import update_airboundary_constructions
from replan2eplus.subsurfaces.presentation import (
    create_subsurface_for_interior_edge,
)
from replan2eplus.examples.subsurfaces import door_details


def test_add_airboundary(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    airboundaries = update_airboundary_constructions(case.idf, [e0], case.zones)
    assert len(airboundaries) == 2
    for boundary in airboundaries:
        assert "Airboundary" in boundary.surface.construction_name
        assert (
            boundary.edge.space_a == e0.space_a and boundary.edge.space_b == e0.space_b
        )
    # ab = airboundaries[0]


# TODO -> test update construction set after airboudnaries are added..


def test_cant_add_subsurfacae_on_airboundary(get_pytest_minimal_case_with_rooms):
    case = get_pytest_minimal_case_with_rooms
    update_airboundary_constructions(case.idf, [e0], case.zones)
    with pytest.raises(IDFMisunderstandingError):
        create_subsurface_for_interior_edge(
            zone_edge, door_details, case.zones, case.idf
        )
