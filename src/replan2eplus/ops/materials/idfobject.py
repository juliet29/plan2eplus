from typing import TypeVar

from geomeppy import IDF
from replan2eplus.idfobjects.base import IDFObject, get_object_description
from dataclasses import dataclass


@dataclass
class IDFMaterialBase(IDFObject):
    Name: str = ""

    # @classmethod
    # def read(cls, idf: IDF, names: list[str] = []): # pyright: ignore[reportIncompatibleMethodOverride]
    #     objects = idf.idfobjects[cls().key]

    #     if names:
    #         return [
    #             cls(**get_object_description(i)) for i in objects if i.Name in names
    #         ]
    #     return [cls(**get_object_description(i)) for i in objects]


@dataclass
class IDFMaterial(IDFMaterialBase):
    Roughness: float = 0.0  # TODO this is an enum!
    Thickness: float = 0.0
    Conductivity: float = 0.0
    Density: float = 0.0
    Specific_Heat: float = 0.0
    Thermal_Absorptance: float = 0.0
    Solar_Absorptance: float = 0.0
    Visible_Absorptance: float = 0.0

    @property
    def key(self):
        return "MATERIAL"


@dataclass
class IDFMaterialNoMass(IDFMaterialBase):
    Roughness: float = 0.0  # TODO this is an enum!
    Thermal_Resistance: float = 0.0

    @property
    def key(self):
        return "MATERIAL:NOMASS"


@dataclass
class IDFMaterialAirGap(IDFMaterialBase):
    Thermal_Resistance: float = 0.0

    @property
    def key(self):
        return "MATERIAL:AIRGAP"


@dataclass
class IDFWindowMaterialGlazing(IDFMaterialBase):
    Optical_Data_Type: str = ""  # TODO this is an enum!
    Thickness: float = 0.0
    Solar_Transmittance_at_Normal_Incidence: float = 0.0
    Front_Side_Solar_Reflectance_at_Normal_Incidence: float = 0.0
    Back_Side_Solar_Reflectance_at_Normal_Incidence: float = 0.0
    Visible_Transmittance_at_Normal_Incidence: float = 0.0
    Front_Side_Visible_Reflectance_at_Normal_Incidence: float = 0.0
    Back_Side_Visible_Reflectance_at_Normal_Incidence: float = 0.0
    Infrared_Transmittance_at_Normal_Incidence: float = 0.0
    Front_Side_Infrared_Hemispherical_Emissivity: float = 0.0
    Back_Side_Infrared_Hemispherical_Emissivity: float = 0.0
    Conductivity: float = 0.0
    Window_Glass_Spectral_Data_Set_Name: float = 0.0

    @property
    def key(self):
        return "WINDOWMATERIAL:GLAZING"


@dataclass
class IDFWindowMaterialGas(IDFMaterialBase):
    Gas_Type: str = ""  # TODO this is an enum!
    Thickness: float = 0.0

    @property
    def key(self):
        return "WINDOWMATERIAL:GAS"


IDFMaterialType = TypeVar("IDFMaterialType", bound=IDFMaterialBase)

material_objects: list[IDFMaterialType] = [  # pyright: ignore[reportGeneralTypeIssues]
    IDFMaterial,
    IDFMaterialNoMass,
    IDFMaterialAirGap,
    IDFWindowMaterialGlazing,
    IDFWindowMaterialGas,
]
