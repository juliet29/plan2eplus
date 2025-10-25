import pytest
from replan2eplus.errors import IDFMisunderstandingError
from replan2eplus.ex.subsurfaces import e0, zone_edge
from replan2eplus.ops.airboundary.presentation import update_airboundary_constructions
from replan2eplus.ops.subsurfaces.logic.interior import (
    create_subsurface_for_interior_edge,
)
from replan2eplus.ex.subsurfaces import door_details
from replan2eplus.ex.main import Cases


def test_add_airboundary():
    case = Cases().two_room
    airboundaries = update_airboundary_constructions(case.idf, [e0], case.objects.zones)
    assert len(airboundaries) == 2
    for boundary in airboundaries:
        assert "Airboundary" in boundary.surface.construction_name
        assert (
            boundary.edge.space_a == e0.space_a and boundary.edge.space_b == e0.space_b
        )
    # ab = airboundaries[0]


# TODO -> test update construction set after airboudnaries are added..


def test_cant_add_subsurfacae_on_airboundary():
    case = Cases().two_room
    update_airboundary_constructions(case.idf, [e0], case.objects.zones)
    with pytest.raises(IDFMisunderstandingError):
        create_subsurface_for_interior_edge(
            zone_edge, door_details, case.objects.zones, case.objects.surfaces, case.idf
        )

if __name__ == "__main__":
    test_add_airboundary()