from geomeppy import IDF
from replan2eplus.idfobjects.base import IDFObject, get_object_description
from dataclasses import dataclass
from typing import Literal


DEFAULT_DISCHARGE_COEFF = 1
DEFAULT_AIR_MASS_FLOW_COEFF = 0.001  # 10E-2  kg/s-m
DEFAULT_MIN_DENSITY_DIFFERENCE = 0.0001  # 10E^-3 kg/m3


@dataclass
class IDFAFNSimulationControl(IDFObject):
    Name: str = "Default"
    AirflowNetwork_Control: Literal["MultizoneWithoutDistribution"] = (
        "MultizoneWithoutDistribution"
    )
    Building_Type: Literal["LowRise", "HighRise"] = "LowRise"
    Azimuth_Angle_of_Long_Axis_of_Building: float = 0
    Ratio_of_Building_Width_Along_Short_Axis_to_Width_Along_Long_Axis: float = (
        1  # 1 => square aspect ratio
    )
    # TODO this should be calculated! -> but do experiment to see how much it matters...

    @property
    def key(self):
        return "AIRFLOWNETWORK:SIMULATIONCONTROL"


@dataclass
class IDFAFNZone(IDFObject):
    Zone_Name: str = ""
    Ventilation_Control_Mode: Literal["Constant", "NoVent"] = (
        "Constant"  # Constant -> depends on venting availability schedule
    )
    Venting_Availability_Schedule_Name: str = (
        ""  # TODO dont add if its none..  #TODO add venting availability schedules..
    )

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:ZONE"


@dataclass
class IDFAFNSimpleOpening(IDFObject):
    Name: str = ""  # subsurface name -> simple opening..
    Discharge_Coefficient: float = 1
    Air_Mass_Flow_Coefficient_When_Opening_is_Closed: float = DEFAULT_DISCHARGE_COEFF
    Minimum_Density_Difference_for_TwoWay_Flow: float = DEFAULT_MIN_DENSITY_DIFFERENCE

    # @property
    # def __post_init__(self):
    #     self.Name = self.create_name(self.Name)

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:COMPONENT:SIMPLEOPENING"


@dataclass
class IDFAFNSurface(IDFObject):
    Surface_Name: str = ""  # subsurface name
    Leakage_Component_Name: str = ""  # has to been in AFN simple opening!
    Ventilation_Control_Mode: Literal["ZoneLevel", "NoVent", "Constant"] = "ZoneLevel"
    External_Node_Name: str = ""

    # NOTE -> can do temperature / enthalpy based controls..
    # here is where can add schedule

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:SURFACE"

    # @classmethod
    # def read(cls, idf: IDF, *args, **kwargs):
    #     objects = idf.idfobjects[cls().key]

    #     def filter_d(d: dict):
    #         return {k: v for k, v in d.items() if k in cls().values.keys()}

    #     return [cls(**filter_d(get_object_description(i))) for i in objects]
