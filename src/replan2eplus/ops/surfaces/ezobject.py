from dataclasses import dataclass
from typing import get_args

from replan2eplus.errors import BadlyFormatedIDFError
from replan2eplus.ezobjects.name import decompose_idf_name
from replan2eplus.geometry.coords import Coordinate3D
from replan2eplus.geometry.directions import WallNormal
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.ezobject_domain import (
    compute_unit_normal,
    create_domain_from_coords,
)

# from replan2eplus.ops.airboundary.idfobject
from replan2eplus.ops.airboundary.interfaces import DEFAULAT_AIRBOUNDARY_NAME
from replan2eplus.ops.surfaces.interfaces import (
    SurfaceCoords,
    SurfaceType,
    OutsideBoundaryCondition,
)


def get_surface_domain(name: str, surface_coords: SurfaceCoords):
    coords = [Coordinate3D(*i) for i in surface_coords]
    try:
        unit_normal_drn = compute_unit_normal(
            [coord.as_three_tuple for coord in coords]
        )
    except KeyError:
        raise BadlyFormatedIDFError(
            f"Invalid unit normal -> are the coords alright for {name}?: {coords}"
        )
    return create_domain_from_coords(unit_normal_drn, coords)


@dataclass
class Surface:
    surface_name: str
    surface_type: SurfaceType
    zone_name: str
    construction_name: str

    boundary_condition: OutsideBoundaryCondition
    boundary_condition_object: str

    original_azimuth: float
    coords: SurfaceCoords
    subsurfaces: list[str]

    ## :**********   Representation **********

    def __rich_repr__(self):
        yield "display_name", self.display_name
        yield "surface_name", self.surface_name
        yield "zone_name", self.zone_name
        yield "domain", self.domain
        yield "surface_type", self.surface_type
        yield "construction", self.construction_name
        yield "neighbor", self.neighbor_name
        yield "subsurfaces", self.subsurfaces

    def __str__(self):
        idf_name = decompose_idf_name(self.surface_name)
        # num = idf_name.full_number
        return f"{idf_name.plan_name}_{self.direction.name}"

    @property
    def display_name(self):
        idf_name = decompose_idf_name(self.surface_name)
        # num = idf_name.full_number
        return f"{idf_name.plan_name}\n{self.direction.name}"  # + num

    ## :********** Associations **********

    @property
    def neighbor_name(self):
        if self.boundary_condition == "surface":
            return str(self.boundary_condition_object)  #
        else:
            return None

    @property
    def room_name(self):
        return decompose_idf_name(self.surface_name).plan_name

    @property
    def room_name_of_neighbor(self):
        if self.neighbor_name:
            return decompose_idf_name(self.neighbor_name).plan_name
        return None

    @property
    def is_airboundary(self):
        return self.construction_name == DEFAULAT_AIRBOUNDARY_NAME

    ## :********** Geometry **********

    @property
    def domain(self):
        domain = get_surface_domain(self.surface_name, self.coords)
        # NOTE: ASSUMING THAT ALL SUBSURFACES / SURFACES ARE WALLS. then will not have an ortho domain
        if self.surface_type == "wall":
            assert isinstance(domain, Domain)
        return domain

    @property
    def azimuth(self):
        return round(float(self.original_azimuth))

    @property
    def direction(self):
        match self.surface_type:
            case "floor":
                return WallNormal.DOWN
            case "roof":
                return WallNormal.UP
            case "wall":
                return WallNormal(self.azimuth)
            case _:
                raise BadlyFormatedIDFError(
                    f"Invalid surface type: recieved: {self.surface_type}. Expected {get_args(SurfaceType)}"
                )
