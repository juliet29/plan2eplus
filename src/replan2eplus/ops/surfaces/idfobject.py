from dataclasses import dataclass, field
from replan2eplus.ops.base import (
    IDFObject,
    filter_relevant_values,
    get_object_description,
)

# from eppy.bunch_subclass import EpBunch
from replan2eplus.ops.surfaces.ezobject import Surface
from geomeppy import IDF
from replan2eplus.ops.surfaces.interfaces import (
    SurfaceCoords,
    SurfaceType,
    OutsideBoundaryCondition,
)


@dataclass
class IDFSurface(IDFObject):
    Name: str = ""
    Surface_Type: SurfaceType = "wall"
    Construction_Name: str = ""
    Zone_Name: str = ""
    Space_Name: str = ""
    Outside_Boundary_Condition: OutsideBoundaryCondition = "surface"
    Outside_Boundary_Condition_Object: str = ""

    azimuth: float = 0
    coords: SurfaceCoords = field(
        default_factory=list
    )  
    subsurfaces: list[str] = field(default_factory=list)

    @property
    def key(self):
        return "BUILDINGSURFACE:DETAILED"

    @classmethod
    def read(cls, idf: IDF, names: list[str] = []):  # pyright: ignore[reportIncompatibleMethodOverride]
        def create_new_objects(o):
            key_values = get_object_description(o)
            properties = {
                "azimuth": o.azimuth,
                "coords": o.coords,
                "subsurfaces": [i.Name for i in o.subsurfaces],
            }
            # filter based on class attributes..  
            relevant_values = filter_relevant_values(key_values, cls().values)

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

    @classmethod
    def get_surface_subsurfaces(cls, idf, name):
        obj = cls().get_one_idf_object(idf, name)
        return obj.subsurfaces  #


# OutsideBiundaryCondition Literal["Adiabatic", "Surface", "Outdoors", "Ground", "Founation", ""]
