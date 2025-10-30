from replan2eplus.idfobjects.base import IDFObject
from typing import Literal


class IDFOutputVariable(IDFObject):
    Key_Value = "*"
    Variable_Name: str = ""
    Reporting_Frequency: Literal[
        "Timestep", "Hourly", "Daily", "Monthly", "RunPeriod", "Environment", "Annual"
    ] = "Timestep"

    @property
    def key(self):
        return "OUTPUT:VARIABLE"


class IDFOutputSQL(IDFObject):
    Option_Type: Literal["Simple", "SimpleAndTabular"] = "Simple"

    @property
    def key(self):
        return "OUTPUT:SQLITE"
