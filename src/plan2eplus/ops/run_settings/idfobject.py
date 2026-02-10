from plan2eplus.ops.base import IDFObject
from dataclasses import dataclass
from geomeppy import IDF


@dataclass
class IDFRunPeriod(IDFObject):
    Name: str = ""
    Begin_Month: int = 1
    End_Month: int = 1
    Begin_Day_of_Month: int = 1
    End_Day_of_Month: int = 1

    @property
    def key(self):
        return "RUNPERIOD"


@dataclass
class IDFLocation(IDFObject):
    Name: str = ""
    Latitude: float = 0.0
    Longitude: float = 0.0
    Time_Zone: float = 0.0
    Elevation: float = 0.0

    @property
    def key(self):
        return "SITE:LOCATION"
