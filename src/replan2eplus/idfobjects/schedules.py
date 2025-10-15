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


@dataclass
class ScheduleFileObject:
    Name: str
    Schedule_Type_Limits_Name: str
    File_Name: Path
    Column_Number: int = 1
    Number_of_Hours_of_Data: int = 8760

    # TODO validate path? and file? # entries = Numbe of Hours or ecven set? 

    @property
    def values(self):
        return self.__dict__


# TODO constant schedule
