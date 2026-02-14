from plan2eplus.ops.base import IDFObject
from dataclasses import dataclass
from typing import Literal
from geomeppyupdated import IDF

# TODO => should be in a config?
# TODO these are things that should be in paper as well
DEFAULT_DISCHARGE_COEFF = 1
DEFAULT_AIR_MASS_FLOW_COEFF = 0.001  # 10E-2  kg/s-m
DEFAULT_MIN_DENSITY_DIFFERENCE = 0.0001  # 10E^-3 kg/m3


@dataclass
class IDFAFNSimulationControl(IDFObject):
    """
    Wind Pressure Coefficient Type ---
    - SurfaceAverageCalculation: then AFN assumes a rectangular boundary and computes coefficients accordingly
    - Input: then AFN expects External Nodes, WPC Array, and WPC Values [DEFAULT, defaults are given]

    Height Selection for Local Wind Pressure Calculation -----
    - ExternalNode: Height given in ExternalNode object will be used
    - OpeningHeight: Opening height of the relevant surface will be used [DEFAULT]

    Building Type ----
    **Used only if Wind Pressure Coefficient Type == SurfaceAverageCalculation**

    Azimuth_Angle_of_Long_Axis_of_Building ---
    **Used only if Wind Pressure Coefficient Type == SurfaceAverageCalculation**
    - Indicates if the building is rotated when the pressure coefficients are calculated


    """

    Name: str = "Default"
    AirflowNetwork_Control: Literal["MultizoneWithoutDistribution"] = (
        "MultizoneWithoutDistribution"  # only relevant option for this package..
    )
    Wind_Pressure_Coefficient_Type: Literal["Input", "SurfaceAverageCalculation"] = (
        "Input"
    )
    Height_Selection_for_Local_Wind_Pressure_Calculation: Literal[
        "ExternalNode", "OpeningHeight"
    ] = "OpeningHeight"
    Building_Type: Literal["LowRise", "HighRise"] = "LowRise"
    Azimuth_Angle_of_Long_Axis_of_Building: float = 0
    Ratio_of_Building_Width_Along_Short_Axis_to_Width_Along_Long_Axis: float = (
        1  # 1 => square aspect ratio  # TODO this should be calculated! -> but do experiment to see how much it matters...
    )

    @property
    def key(self):
        return "AIRFLOWNETWORK:SIMULATIONCONTROL"


@dataclass
class IDFAFNZone(IDFObject):
    """
    Ventilation Control Mode ----
    - ZoneLevel: Zone controls
    - Constant: Uses the ventilation availability schedule
    """

    Zone_Name: str = ""
    Ventilation_Control_Mode: Literal["Constant", "NoVent"] = "Constant"
    Venting_Availability_Schedule_Name: str = ""

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:ZONE"


@dataclass
class IDFAFNSimpleOpening(IDFObject):
    # NOTE: this is one of many types of "Leakage Components" -> gets linked to the afn surface. # TODO: does its geometry matter?
    Name: str = ""
    Discharge_Coefficient: float = DEFAULT_DISCHARGE_COEFF
    Air_Mass_Flow_Coefficient_When_Opening_is_Closed: float = (
        DEFAULT_AIR_MASS_FLOW_COEFF  # how does this influence?
    )
    Minimum_Density_Difference_for_TwoWay_Flow: float = DEFAULT_MIN_DENSITY_DIFFERENCE

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:COMPONENT:SIMPLEOPENING"


@dataclass
class IDFAFNSurface(IDFObject):
    """
    Surface Name ----
    - Refers to an existing surface or subsurface

    Ventilation Control Mode ----
    - ZoneLevel: Zone controls
    - Constant: This is needed to set venting availability on a zone by zone level
    """

    Surface_Name: str = ""
    Leakage_Component_Name: str = ""
    Ventilation_Control_Mode: Literal["ZoneLevel", "NoVent", "Constant"] = "Constant"
    External_Node_Name: str = ""
    Venting_Availability_Schedule_Name: str = ""

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:SURFACE"

    @classmethod
    def update_afn_surface(
        cls,
        idf: IDF,
        object_name: str,
        param: Literal["External_Node_Name", "Venting_Availability_Schedule_Name"],
        new_value: str,
    ):
        cls().update(idf, object_name, param, new_value, identifier="Surface_Name")


@dataclass
class IDFAFNExternalNode(IDFObject):
    """
    Wind angle is considered to be the absolute wind angle. Not the relative angle between the listed direction and any given surface.

    External Node Height -----
    - By default, relative pressure is calculated at the zone height
    """

    Name: str = ""
    External_Node_Height: float = 0.0
    Wind_Pressure_Coefficient_Curve_Name: str = ""

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:EXTERNALNODE"


FALSE_VALUE = -1000


@dataclass
class IDFAFNWindPressureCoefficientValues(IDFObject):
    """
    Used only if Wind Pressure Coefficient Type  = Input in AirflowNetwork Simulation Control Object

    Number of inputs must correspond to number of wind directions in the Wind Pressure Coefficient Array Object
    """

    Name: str = ""
    AirflowNetworkMultiZoneWindPressureCoefficientArray_Name: str = (
        ""  # TODO see how eppy handles this name, because originally is separated by colons.. not allowed in Pthon
    )
    Wind_Pressure_Coefficient_Value_1: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_2: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_3: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_4: float = FALSE_VALUE

    Wind_Pressure_Coefficient_Value_5: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_6: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_7: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_8: float = FALSE_VALUE

    Wind_Pressure_Coefficient_Value_9: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_10: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_11: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_12: float = FALSE_VALUE

    Wind_Pressure_Coefficient_Value_13: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_14: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_15: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_16: float = FALSE_VALUE

    Wind_Pressure_Coefficient_Value_17: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_18: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_19: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_20: float = FALSE_VALUE

    Wind_Pressure_Coefficient_Value_21: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_22: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_23: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_24: float = FALSE_VALUE

    Wind_Pressure_Coefficient_Value_25: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_26: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_27: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_28: float = FALSE_VALUE

    Wind_Pressure_Coefficient_Value_29: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_30: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_31: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_32: float = FALSE_VALUE

    Wind_Pressure_Coefficient_Value_33: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_34: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_35: float = FALSE_VALUE
    Wind_Pressure_Coefficient_Value_36: float = FALSE_VALUE

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:WINDPRESSURECOEFFICIENTVALUES"

    @property
    def values(self):
        return {
            k: v
            for k, v in self.__dict__.items()
            if isinstance(v, str) or v > FALSE_VALUE
        }


@dataclass
class IDFAFNWindPressureCoefficientArray(IDFObject):
    """
    Used only if Wind Pressure Coefficient Type  = Input in AirflowNetwork Simulation Control Object

    Number of inputs must correspond to number of wind directions in the Wind Pressure Coefficient Values Object
    """

    Name: str = ""
    Wind_Direction_1: float = FALSE_VALUE
    Wind_Direction_2: float = FALSE_VALUE
    Wind_Direction_3: float = FALSE_VALUE
    Wind_Direction_4: float = FALSE_VALUE

    Wind_Direction_5: float = FALSE_VALUE
    Wind_Direction_6: float = FALSE_VALUE
    Wind_Direction_7: float = FALSE_VALUE
    Wind_Direction_8: float = FALSE_VALUE

    Wind_Direction_9: float = FALSE_VALUE
    Wind_Direction_10: float = FALSE_VALUE
    Wind_Direction_11: float = FALSE_VALUE
    Wind_Direction_12: float = FALSE_VALUE

    Wind_Direction_13: float = FALSE_VALUE
    Wind_Direction_14: float = FALSE_VALUE
    Wind_Direction_15: float = FALSE_VALUE
    Wind_Direction_16: float = FALSE_VALUE

    Wind_Direction_17: float = FALSE_VALUE
    Wind_Direction_18: float = FALSE_VALUE
    Wind_Direction_19: float = FALSE_VALUE
    Wind_Direction_20: float = FALSE_VALUE

    Wind_Direction_21: float = FALSE_VALUE
    Wind_Direction_22: float = FALSE_VALUE
    Wind_Direction_23: float = FALSE_VALUE
    Wind_Direction_24: float = FALSE_VALUE

    Wind_Direction_25: float = FALSE_VALUE
    Wind_Direction_26: float = FALSE_VALUE
    Wind_Direction_27: float = FALSE_VALUE
    Wind_Direction_28: float = FALSE_VALUE

    Wind_Direction_29: float = FALSE_VALUE
    Wind_Direction_30: float = FALSE_VALUE
    Wind_Direction_31: float = FALSE_VALUE
    Wind_Direction_32: float = FALSE_VALUE

    Wind_Direction_33: float = FALSE_VALUE
    Wind_Direction_34: float = FALSE_VALUE
    Wind_Direction_35: float = FALSE_VALUE
    Wind_Direction_36: float = FALSE_VALUE

    @property
    def key(self):
        return "AIRFLOWNETWORK:MULTIZONE:WINDPRESSURECOEFFICIENTARRAY"

    @property
    def values(self):
        return {
            k: v
            for k, v in self.__dict__.items()
            if isinstance(v, str) or v > FALSE_VALUE
        }
