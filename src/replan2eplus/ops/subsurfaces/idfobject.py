from dataclasses import dataclass
from typing import get_args

from replan2eplus.ezobjects.ezbase import EpBunch
from replan2eplus.ops.subsurfaces.interfaces import SubsurfaceKey, SubsurfaceType
from replan2eplus.idfobjects.base import (
    IDFObject,
    filter_relevant_values,
    get_object_description,
)
from utils4plans.lists import chain_flatten
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from utils4plans.lists import get_unique_one
from geomeppy import IDF


@dataclass
class IDFSubsurface(IDFObject):
    Name: str = ""
    Building_Surface_Name: str = ""
    Construction_Name: str = ""
    Starting_X_Coordinate: float = 0
    Starting_Z_Coordinate: float = 0
    Length: float = 0
    Height: float = 0
    # Outside_Boundary_Condition_Object: str
    type_: SubsurfaceType = "Door"  # how do we populate this upon readng? maybe different options get key from type or get key from epobject
    is_interior: bool = False
    original_key: SubsurfaceKey | None = None

    # TODO: TEST! -> have to define a read method..
    @property
    def key(self) -> SubsurfaceKey:
        if self.original_key:
            return self.original_key
        else:
            assert self.type_
        match self.is_interior, self.type_.casefold():
            case False, "door":
                return "DOOR"
            case True, "door":
                return "DOOR:INTERZONE"
            case _, "window":
                return "WINDOW"
            case _:
                raise ValueError(f"Invalid type: {self.type_} ")

    @classmethod
    def read(cls, idf: IDF):  # pyright: ignore[reportIncompatibleMethodOverride]
        objects = chain_flatten([idf.idfobjects[i] for i in get_args(SubsurfaceKey)])

        def get_type(o: EpBunch) -> SubsurfaceType:
            assert o.Name
            return "Door" if "door" in o.Name.lower() else "Window"

        # relevant_values = filter_relevant_values(key_values, cls().values)

        return [
            cls(
                **filter_relevant_values(get_object_description(i), cls().values),
                original_key=i.key,
                type_=get_type(i),
            )
            for i in objects
        ]

    @property
    def values(self):
        d = self.__dict__
        d.pop("type_")
        d.pop("is_interior")
        d.pop("original_key")

        return d

    def create_ezobject(self, surfaces: list[Surface]) -> Subsurface:
        surface = get_unique_one(
            surfaces, lambda x: x.surface_name == self.Building_Surface_Name
        )
        return Subsurface(
            self.Name,
            self.Construction_Name,
            self.Starting_X_Coordinate,
            self.Starting_Z_Coordinate,
            self.Length,
            self.Height,
            # self.Outside_Boundary_Condition_Object,
            self.type_,
            surface,
        )
