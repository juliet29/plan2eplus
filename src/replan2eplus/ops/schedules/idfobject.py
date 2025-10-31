from replan2eplus.ops.base import IDFObject
from dataclasses import dataclass
from typing import NamedTuple, Literal

from pathlib import Path


@dataclass
class IDFScheduleTypeLimits(IDFObject):
    Name: str
    Lower_Limit_Value: int
    Upper_Limit_Value: int
    Numeric_Type: Literal["Continuous", "Discrete"]
    Unit_Type: Literal[
        "Dimensionless",
        "Temperature",
        "DeltaTemperature",
        "PrecipitationRate",
        "Angle",
        "Convection Coefficient",
        "Activity Level",
        "Velocity",
        "Capacity",
        "Power",
        "Availability",
        "Percent",
        "Control",
    ]

    @property
    def key(self):
        return "SCHEDULETYPELIMITS"


@dataclass
class IDFScheduleFile(IDFObject):
    Name: str
    Schedule_Type_Limits_Name: str
    File_Name: Path
    Column_Number: int = 1
    Number_of_Hours_of_Data: int = 8760
    Rows_to_Skip_at_Top: int = 1

    # TODO validate path? and file? # entries = Numbe of Hours or ecven set?

    @property
    def key(self):
        return "SCHEDULE:FILE"

    @property
    def values(self):
        d = self.values
        d["File_Name"] = str(self.File_Name)
        return d

    # @property
    # def key(self) -> str:

@dataclass
class IDFScheduleCompact(IDFObject):
    """
    Example Entry: 
    Field_1: Through: 12/31
    For: AllDays
    Until: 24:00
    
    """
    Name: str
    Schedule_Type_Limits_Name: str
    Field_1: str = ""
    Field_2: str = ""
    Field_3: str = ""
    