from dataclasses import dataclass
from typing import NamedTuple, Literal

from pathlib import Path


# class Until(NamedTuple):
#     Time: int
#     Value: float

#     @property
#     def values(self):
#         return (self.Time, self.Value)


# @dataclass
# class FieldSet:
#     For: Literal[
#         "AllDays", "Weekdays", "Weekends"
#     ]  # TODO can be a list of these as well
#     Through: str  # TODO add type -> has to be date with format: 00/00
#     Until: list[Until]


#     @property
#     def values(self):
#         until_dict = 0
#         d = {
#             "For": self.For,
#             "Through": self.Through,
#         }
class ScheduleTypeLimits(NamedTuple):
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
    def values(self):
        # TODO return key as well?
        return self._asdict()

    @property
    def key(self):
        return "SCHEDULETYPELIMITS"


class ScheduleFileObject(NamedTuple):
    Name: str
    Schedule_Type_Limits_Name: str
    File_Name: Path
    Column_Number: int = 1
    Number_of_Hours_of_Data: int = 8760
    Rows_to_Skip_at_Top:int = 1

    # TODO validate path? and file? # entries = Numbe of Hours or ecven set?

    @property
    def values(self):
        # TODO return key as well?
        d = self._asdict()
        d["File_Name"] = str(self.File_Name)
        return d

    @property
    def key(self):
        return "SCHEDULE:FILE"


# TODO constant schedule
