from dataclasses import dataclass
from typing import NamedTuple
# These are taken from IDD for E+ 22.1
# TODO: is this possible to autogenerate based on the IDD?
# also should these be pydantic? so can have validation and transomation? 

# todo rename! 
@dataclass
class MaterialObjectBase:
    Name: str


@dataclass
class MaterialObject(MaterialObjectBase):
    Roughness: float  # TODO this is an enum!
    Thickness: float
    Conductivity: float
    Density: float
    Specific_Heat: float
    Thermal_Absorptance: float | str = ""
    Solar_Absorptance: float | str = ""
    Visible_Absorptance: float | str = ""


@dataclass
class MaterialNoMassObject(MaterialObjectBase):
    Roughness: float  # TODO this is an enum!
    Thermal_Resistance: float


@dataclass
class MaterialAirGap(MaterialObjectBase):
    Thermal_Resistance: float


@dataclass
class WindowMaterialGlazingObject(MaterialObjectBase):
    Optical_Data_Type: str  # TODO this is an enum!
    Window_Glass_Spectral_Data_Set_Name: float
    Thickness: float
    Solar_Transmittance_at_Normal_Incidence: float
    Front_Side_Solar_Reflectance_at_Normal_Incidence: float
    Back_Side_Solar_Reflectance_at_Normal_Incidence: float
    Visible_Transmittance_at_Normal_Incidence: float
    Front_Side_Visible_Reflectance_at_Normal_Incidence: float
    Back_Side_Visible_Reflectance_at_Normal_Incidence: float
    Infrared_Transmittance_at_Normal_Incidence: float
    Front_Side_Infrared_Hemispherical_Emissivity: float
    Back_Side_Infrared_Hemispherical_Emissivity: float
    Conductivity: float


@dataclass
class WindowMaterialGasObject(MaterialObjectBase):
    Gas_Type: str  # TODO this is an enum!
    Thickness: float




# class MaterialInput(NamedTuple):
#     name: str
#     key: str

#     def material_properties(self):
#         if self.key == "":
#             expected_properties = {}

#     # TODO this will have inheritance -> there are many types of materials!




# @dataclass
# class BaseConstructionSet:
#     default: Construction
#     interior: Construction | None = None
#     exterior: Construction | None = None

#     def __post_init__(self):
#         if not self.interior:
#             self.interior = self.default
#         if not self.exterior:
#             self.exterior = self.default

# @dataclass
# class EPConstructionSet:
#     wall: BaseConstructionSet
#     roof: BaseConstructionSet
#     floor: BaseConstructionSet
#     window: BaseConstructionSet
#     door: BaseConstructionSet
