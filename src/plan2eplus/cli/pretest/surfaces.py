from plan2eplus.ops.surfaces.ezobject import Surface
from loguru import logger


def test_surface_types():
    new_surface = Surface(
        surface_name="test",
        surface_type="Ceiling",
        zone_name="",
        construction_name="",
        boundary_condition="",
        boundary_condition_object="",
        original_azimuth=0,
        coords=[],
        subsurfaces=[],
    )

    logger.debug(new_surface.surface_type)
    logger.debug(new_surface.surface_type.casefold())
    logger.debug(new_surface.direction)
    pass
