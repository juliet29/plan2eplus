from dataclasses import dataclass
from typing import Any, Literal, NamedTuple

from replan2eplus.ops.subsurfaces.ezobject import Edge
from replan2eplus.ops.subsurfaces.interfaces import SubsurfaceKey, SubsurfaceType
from replan2eplus.idfobjects.base import IDFObject
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.subsurfaces.ezobject import Subsurface


@dataclass
class SubsurfaceObject(IDFObject):
    Name: str
    Building_Surface_Name: str
    Starting_X_Coordinate: float
    Starting_Z_Coordinate: float
    Length: float
    Height: float
    Outside_Boundary_Condition_Object: str
    type_: SubsurfaceType  # how do we populate this upon readng? maybe different options get key from type or get key from epobject
    is_interior: bool

    # TODO: TEST!
    @property
    def key(self) -> SubsurfaceKey:
        match self.is_interior, self.type_:
            case False, "Door":
                return "DOOR"
            case True, "Door":
                return "DOOR:INTERZONE"
            case _, "Window":
                return "WINDOW"
            case _:
                raise ValueError(
                    f"Invalid Outside Boundary Condition or type_| Boundary Cond: {self.Outside_Boundary_Condition_Object} type: {self.type_} "
                )

    @property
    def values(self):
        d = self.__dict__
        d.pop("type_")
        return d

    def create_ezobject(self, surface: Surface, edge: Edge) -> Subsurface:
        return Subsurface(
            self.Name,
            self.Starting_X_Coordinate,
            self.Starting_Z_Coordinate,
            self.Length,
            self.Height,
            self.type_,
            surface,
            edge,
        )
