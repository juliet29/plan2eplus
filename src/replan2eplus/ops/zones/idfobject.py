from replan2eplus.ezobjects.surface import Surface as EzSurface
from replan2eplus.idfobjects.base import IDFObject, get_object_description
from dataclasses import dataclass
from geomeppy import IDF
from typing import NamedTuple, TypedDict
from replan2eplus.ezobjects.zone import Zone


@dataclass
class IDFZone(IDFObject):
    Name: str = ""
    Direction_of_Relative_North: int = 0
    X_Origin: float = 0
    Y_Origin: float = 0
    Z_Origin: float = 0
    Type: int = 1
    Multiplier: int = 1
    Ceiling_Height: int | str = "autocalculate"
    Volume: int | str = "autocalculate"
    Floor_Area: int | str = "autocalculate"
    Zone_Inside_Convection_Algorithm: str = ""
    Zone_Outside_Convection_Algorithm: str = ""
    Part_of_Total_Floor_Area: str = "Yes"

    @property
    def key(self):
        return "ZONE"

    def create_ezobject(self, surfaces: list[EzSurface]):
        return Zone(self.Name, surfaces)

    # @classmethod
    # def read(cls, idf: IDF):
    #     objects = idf.idfobjects[cls().key]
    #     return [cls(**get_object_description(i)) for i in objects]


@dataclass
class GeomeppyBlock(IDFObject):
    name: str
    coordinates: list[tuple[float, float]]
    height: float

    def write(self, idf: IDF):
        idf.add_block(**self.values)
        return idf
