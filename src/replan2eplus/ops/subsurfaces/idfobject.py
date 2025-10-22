from dataclasses import dataclass
from typing import Any, Literal, NamedTuple, get_args

from replan2eplus.ezobjects.base import EpBunch
from replan2eplus.ops.subsurfaces.ezobject import Edge
from replan2eplus.ops.subsurfaces.interfaces import SubsurfaceKey, SubsurfaceType
from replan2eplus.idfobjects.base import IDFObject, get_object_description
from utils4plans.lists import chain_flatten
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from utils4plans.lists import get_unique_one
from geomeppy import IDF


@dataclass
class IDFSubsurface(IDFObject):
    Name: str
    Building_Surface_Name: str
    Starting_X_Coordinate: float
    Starting_Z_Coordinate: float
    Length: float
    Height: float
    Outside_Boundary_Condition_Object: str
    type_: SubsurfaceType = ""  # how do we populate this upon readng? maybe different options get key from type or get key from epobject
    is_interior: bool = False
    original_key: SubsurfaceKey | None = None

    # TODO: TEST! -> have to define a read method..
    @property
    def key(self) -> SubsurfaceKey:
        if self.original_key:
            return self.original_key
        else:
            assert self.type_
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

    @classmethod
    def read(cls, idf: IDF):
        objects = chain_flatten([idf.idfobjects[i] for i in get_args(SubsurfaceKey)])

        def get_type(o: EpBunch) -> SubsurfaceType:
            assert o.Name
            return "Door" if "door" in o.Name.lower() else "Window"

        return [
            cls(**get_object_description(i), original_key=i.key, type_=get_type(i))
            for i in objects
        ]

    @property
    def values(self):
        d = self.__dict__
        d.pop("type_")
        d.pop("is_interior")
        return d

    def create_ezobject(self, surfaces: list[Surface]) -> Subsurface:
        surface = get_unique_one(
            surfaces, lambda x: x.surface_name == self.Building_Surface_Name
        )
        return Subsurface(
            self.Name,
            self.Starting_X_Coordinate,
            self.Starting_Z_Coordinate,
            self.Length,
            self.Height,
            self.type_,
            surface,
        )
