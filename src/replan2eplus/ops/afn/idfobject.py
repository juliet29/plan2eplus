from replan2eplus.idfobjects.base import IDFObject
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
    Ratio_of_Building_Width_Along_Short_Axis_to_Width_Along_Long_Axis: float = 1  # 1 => square aspect ratio  # TODO this should be calculated! -> but do experiment to see how much it matters...
    Wind_Pressure_Coefficient_Type: str = ""
    Height_Selection_for_Local_Wind_Pressure_Calculation: Literal[
        "ExternalNode", "OpeningHeight"
    ] = "OpeningHeight"

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
    # NOTE: this is one of many types of leakage components -> gets linked to the afn surface
    Name: str = ""
    Discharge_Coefficient: float = 1
    Air_Mass_Flow_Coefficient_When_Opening_is_Closed: float = (
        DEFAULT_DISCHARGE_COEFF  # how does this influence?
    )
    Minimum_Density_Difference_for_TwoWay_Flow: float = DEFAULT_MIN_DENSITY_DIFFERENCE

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:COMPONENT:SIMPLEOPENING"


@dataclass
class IDFAFNSurface(IDFObject):
    Surface_Name: str = ""
    Leakage_Component_Name: str = ""
    Ventilation_Control_Mode: Literal["ZoneLevel", "NoVent", "Constant"] = "ZoneLevel"
    # needs to be `Constant` when setting a venting availabily schedule on a per surface basis.. -> this is most applicable for doors.. q
    External_Node_Name: str = ""
    Venting_Availability_Schedule_Name = ""

    # NOTE -> can do temperature / enthalpy based controls..
    # here is where can add schedule

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:SURFACE"


@dataclass
class IDFAFNExternalNode(IDFObject):
    """
    Wind angle is considered to be the absolute wind angle. Not the relative angle between the listed direction and any given surface.
    """

    Name: str = ""
    External_Node_Height: float = (
        0.0  # by default, relative pressure is calculated at the zone height
    )
    Wind_Pressure_Coefficient_Curve_Name = ""

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:EXTERNALNODE"


@dataclass
class IDFAFNWindPressureCoefficientValues(IDFObject):
    """
    Used only if Wind Pressure Coefficient Type  = Input in AirflowNetwork Simulation Control Object

    Number of inputs must correspond to number of wind directions in the Wind Pressure Coefficient Array Object
    """

    Name: str = ""
    AirflowNetwork_MultiZone_WindPressureCoefficientArray_Name = ""  # TODO see how eppy handles this name, because originally is separated by colons.. not allowed in Pthon
    Wind_Pressure_Coefficient_Value_1: float = 0.0
    Wind_Pressure_Coefficient_Value_2: float = 0.0
    Wind_Pressure_Coefficient_Value_3: float = 0.0
    Wind_Pressure_Coefficient_Value_4: float = 0.0

    Wind_Pressure_Coefficient_Value_5: float = 0.0
    Wind_Pressure_Coefficient_Value_6: float = 0.0
    Wind_Pressure_Coefficient_Value_7: float = 0.0
    Wind_Pressure_Coefficient_Value_8: float = 0.0

    Wind_Pressure_Coefficient_Value_9: float = 0.0
    Wind_Pressure_Coefficient_Value_10: float = 0.0
    Wind_Pressure_Coefficient_Value_11: float = 0.0
    Wind_Pressure_Coefficient_Value_12: float = 0.0

    Wind_Pressure_Coefficient_Value_13: float = 0.0
    Wind_Pressure_Coefficient_Value_14: float = 0.0
    Wind_Pressure_Coefficient_Value_15: float = 0.0
    Wind_Pressure_Coefficient_Value_16: float = 0.0

    Wind_Pressure_Coefficient_Value_17: float = 0.0
    Wind_Pressure_Coefficient_Value_18: float = 0.0
    Wind_Pressure_Coefficient_Value_19: float = 0.0
    Wind_Pressure_Coefficient_Value_20: float = 0.0

    Wind_Pressure_Coefficient_Value_21: float = 0.0
    Wind_Pressure_Coefficient_Value_22: float = 0.0
    Wind_Pressure_Coefficient_Value_23: float = 0.0
    Wind_Pressure_Coefficient_Value_24: float = 0.0

    Wind_Pressure_Coefficient_Value_25: float = 0.0
    Wind_Pressure_Coefficient_Value_26: float = 0.0
    Wind_Pressure_Coefficient_Value_27: float = 0.0
    Wind_Pressure_Coefficient_Value_28: float = 0.0

    Wind_Pressure_Coefficient_Value_29: float = 0.0
    Wind_Pressure_Coefficient_Value_30: float = 0.0
    Wind_Pressure_Coefficient_Value_31: float = 0.0
    Wind_Pressure_Coefficient_Value_32: float = 0.0

    Wind_Pressure_Coefficient_Value_33: float = 0.0
    Wind_Pressure_Coefficient_Value_34: float = 0.0
    Wind_Pressure_Coefficient_Value_35: float = 0.0
    Wind_Pressure_Coefficient_Value_36: float = 0.0

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:WINDPRESSURECOEFFICIENTVALUES"


@dataclass
class IDFAFNWindPressureCoefficientArray(IDFObject):
    """
    Used only if Wind Pressure Coefficient Type  = Input in AirflowNetwork Simulation Control Object

    Number of inputs must correspond to number of wind directions in the Wind Pressure Coefficient Values Object
    """

    Name: str = ""
    Wind_Direction_1: float = 0.0
    Wind_Direction_2: float = 0.0
    Wind_Direction_3: float = 0.0
    Wind_Direction_4: float = 0.0

    Wind_Direction_5: float = 0.0
    Wind_Direction_6: float = 0.0
    Wind_Direction_7: float = 0.0
    Wind_Direction_8: float = 0.0

    Wind_Direction_9: float = 0.0
    Wind_Direction_10: float = 0.0
    Wind_Direction_11: float = 0.0
    Wind_Direction_12: float = 0.0

    Wind_Direction_13: float = 0.0
    Wind_Direction_14: float = 0.0
    Wind_Direction_15: float = 0.0
    Wind_Direction_16: float = 0.0

    Wind_Direction_17: float = 0.0
    Wind_Direction_18: float = 0.0
    Wind_Direction_19: float = 0.0
    Wind_Direction_20: float = 0.0

    Wind_Direction_21: float = 0.0
    Wind_Direction_22: float = 0.0
    Wind_Direction_23: float = 0.0
    Wind_Direction_24: float = 0.0

    Wind_Direction_25: float = 0.0
    Wind_Direction_26: float = 0.0
    Wind_Direction_27: float = 0.0
    Wind_Direction_28: float = 0.0

    Wind_Direction_29: float = 0.0
    Wind_Direction_30: float = 0.0
    Wind_Direction_31: float = 0.0
    Wind_Direction_32: float = 0.0

    Wind_Direction_33: float = 0.0
    Wind_Direction_34: float = 0.0
    Wind_Direction_35: float = 0.0
    Wind_Direction_36: float = 0.0

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:WINDPRESSURECOEFFICIENTVALUES"
