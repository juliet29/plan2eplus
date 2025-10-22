from dataclasses import dataclass, field
from eppy.bunch_subclass import EpBunch
from replan2eplus.idfobjects.base import IDFObject, get_object_description
from replan2eplus.ops.surfaces.ezobject import Surface
from geomeppy import IDF
from replan2eplus.ops.surfaces.interfaces import (
    SurfaceCoords,
    SurfaceType,
    WindExposure,
    SunExposure,
    OutsideBoundaryCondition,
)


@dataclass
class IDFSurface(IDFObject):
    Name: str = ""
    Surface_Type: SurfaceType = "Wall"
    Construction_Name: str = ""
    Zone_Name: str = ""
    Space_Name: str = ""
    Outside_Boundary_Condition: OutsideBoundaryCondition = "Surface"
    Outside_Boundary_Condition_Object: str = ""

    azimuth: float = 0
    coords: SurfaceCoords = field(
        default_factory=list
    )  # TODO this is wrong, check this..
    subsurfaces: list[str] = field(default_factory=list)

    @property
    def key(self):
        return "BUILDINGSURFACE:DETAILED"

    @classmethod
    def read(cls, idf: IDF, names: list[str] = []):
        def create_new_objects(o):
            key_values = get_object_description(o)
            properties = {
                "azimuth": o.azimuth,
                "coords": o.coords,
                "subsurfaces": o.subsurfaces,
            }
            # filter based on class attributes.. -> #TODO move to base after test.
            relevant_values = { 
                k: v for k, v in key_values.items() if k in cls().values.keys()
            }
            d = relevant_values | properties

            return cls(**d)

        objects = idf.idfobjects[cls().key]
        if names:   
            return [create_new_objects(o) for o in objects if o.Name in names]
        
        return [create_new_objects(o) for o in objects] 

    def create_ezobject(self):
        return Surface(
            self.Name,
            self.Surface_Type,
            self.Zone_Name,
            self.Construction_Name,
            self.Outside_Boundary_Condition,
            self.Outside_Boundary_Condition_Object,
            self.azimuth,
            self.coords,
            self.subsurfaces,
        )


# OutsideBiundaryCondition Literal["Adiabatic", "Surface", "Outdoors", "Ground", "Founation", ""]
