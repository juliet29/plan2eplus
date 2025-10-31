from replan2eplus.ex.ortho_domain import ortho_room
from replan2eplus.geometry.ortho_domain import OrthoDomain
from replan2eplus.geometry.shapely_bounds import ShapelyBounds


def test_create_bounding_domain():
    domain = ortho_room.domain
    assert isinstance(domain, OrthoDomain)

    expected_domain = ShapelyBounds(1, 1, 3, 3).domain
    assert expected_domain == domain.bounding_domain
