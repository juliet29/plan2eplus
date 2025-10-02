from replan2eplus.geometry.domain import Domain
from replan2eplus.ops.airboundary.interfaces import DEFAULT_AIRBOUNDARY_OBJECT
from replan2eplus.ezobjects.base import EZObject
from dataclasses import dataclass
import replan2eplus.epnames.keys as epkeys
from enum import StrEnum, Enum
from typing import Literal
from replan2eplus.errors import IDFMisunderstandingError, BadlyFormatedIDFError
from eppy.bunch_subclass import EpBunch
from replan2eplus.geometry.coords import Coordinate3D
from replan2eplus.geometry.directions import WallNormal
from replan2eplus.geometry.ezobject_domain import compute_unit_normal, create_domain_from_coords

from rich.table import Table


def get_surface_coords(surface: EpBunch):
    surf_coords = surface.coords
    assert surf_coords
    return [Coordinate3D(*i) for i in surf_coords]


def get_surface_domain(surface: EpBunch):
    coords = get_surface_coords(surface)
    try:
        unit_normal_drn = compute_unit_normal(
            [coord.as_three_tuple for coord in coords]
        )
    except KeyError:
        raise BadlyFormatedIDFError(
            f"Invalid unit normal -> are the coords alright for {surface.Name}?: {coords}"
        )
    return create_domain_from_coords(unit_normal_drn, coords)



# NOTE: this code showcases what could be a recurring pattern for wrapping geomeppy/eppy outputs -> has to be returned in an enum, but then can access using string literals and get hints
# This is safe if a type checker is being used and makes coding easier, but then literals are floating everywhere, pros + cons..


SurfaceBoundaryCondition = StrEnum(
    "SurfaceBoundaryCondition", "surface ground outdoors"
)
SurfaceBoundaryConditionNames = Literal["surface", "ground", "outdoors"]

# StrEnum()

SurfaceType = StrEnum("SurfaceType", "floor roof wall")
SurfaceTypeNames = Literal["floor", "roof", "wall"]


@dataclass
class Surface(EZObject):
    # TODO turn to class (instead of) if have to init later..?  / read python docs..
    _epbunch: EpBunch
    expected_key: str = epkeys.SURFACE

    def __post_init__(self):
        assert self.expected_key == epkeys.SURFACE

    def __rich_repr__(self):
        yield "display_name", self.display_name
        yield "surface_name", self.surface_name
        yield "zone_name", self.zone_name
        yield "domain", self.domain
        yield "num_subsurfaces", len(self.subsurface_names)
        yield "type_", self.type_
        yield "is_airboundary", self.is_airboundary
        yield "neighbor", self.neighbor
        yield "subsurface_names", self.subsurface_names

    @property
    def surface_name(self):
        return self._idf_name

    @property
    def zone_name(self):
        return self._epbunch.Zone_Name

    @property
    def domain(self):
        domain =  get_surface_domain(self._epbunch)
        # NOTE: ASSUMING THAT ALL SUBSURFACES / SURFACES ARE WALLS. then will not have an ortho domain 
        if self.type_ == "wall":
            assert isinstance(domain, Domain)
        return domain 

    @property
    def type_(self) -> SurfaceTypeNames:
        return SurfaceType(self._epbunch.Surface_Type).name

    @property
    def azimuth(self):
        return round(float(self._epbunch.azimuth))

    @property
    def direction(self):
        match self.type_:
            case "floor":
                return WallNormal.DOWN
            case "roof":
                return WallNormal.UP
            case "wall":
                return WallNormal(self.azimuth)
            case _:
                raise BadlyFormatedIDFError("Invalid surface type!")

    @property
    def display_name(self):
        # num = f"-{self._dname.position_number}" if self._dname.position_number else ""
        num = self._dname.full_number
        return f"{self._dname.plan_name}\n{self.direction.name}" + num

    @property
    def error_string(self):
        # TODO make this handle having a name, and make it a proper table with demarcations..
        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_column(justify="left")
        grid.add_row("Zone", f"{self.zone_name}")
        grid.add_row("Direction", f"{self.direction.name}")
        grid.add_row("Number", f"{self._dname.full_number}")
        grid.add_row("Domain", f"{self.domain}")
        return grid

    @property
    def boundary_condition(self) -> SurfaceBoundaryConditionNames:
        return SurfaceBoundaryCondition(self._epbunch.Outside_Boundary_Condition).name

    @property
    def neighbor(self):
        if self.boundary_condition == "surface":
            return str(self._epbunch.Outside_Boundary_Condition_Object)  #
        else:
            return None

    @property
    def subsurface_names(self):
        return [i.Name for i in self._epbunch.subsurfaces]  # type: ignore

    @property
    def construction_name(self):
        return self._epbunch.Construction_Name

    @property
    def is_airboundary(self):
        return self.construction_name == DEFAULT_AIRBOUNDARY_OBJECT.Name

    # def update_construction(self, construction_name: str):
    #     pass


# def segment_surfaces(surfaces: list[Surface]):
#     return sort_and_group_objects(surfaces, lambda x: x.type_)
