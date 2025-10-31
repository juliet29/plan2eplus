from dataclasses import dataclass
from geomeppy import IDF
from replan2eplus.ops.base import IDFObject
from typing import Literal


# TODO check if this is needed..
def is_surface_or_zone_wind(name):
    if "Wind" in name:
        if "Zone" in name or "Surace" in name:
            return True


@dataclass
class IDFOutputVariable(IDFObject):
    Key_Value: str = "*"
    Variable_Name: str = ""
    Reporting_Frequency: Literal[
        "Timestep", "Hourly", "Daily", "Monthly", "RunPeriod", "Environment", "Annual"
    ] = "Timestep"

    @property
    def key(self):
        return "OUTPUT:VARIABLE"

    def get_existing_output_variable_names(self, idf: IDF):
        return [o.Variable_Name for o in self.get_idf_objects(idf)]

    def correct_timestep_for_wind_variables(self):
        if is_surface_or_zone_wind(self.Variable_Name):
            self.Reporting_Frequency = "Hourly"

    def check_and_write(self, idf: IDF):
        f"checking if var {self.Variable_Name} exists..."
        if self.Variable_Name not in self.get_existing_output_variable_names(idf):
            f"{self.Variable_Name} exists"
            self.correct_timestep_for_wind_variables()
            self.write(idf)


@dataclass
class IDFOutputSQL(IDFObject):
    Option_Type: Literal["Simple", "SimpleAndTabular"] = "Simple"

    @property
    def key(self):
        return "OUTPUT:SQLITE"

    def check_and_write(self, idf: IDF):
        existing = self.get_idf_objects(idf)
        if not existing:
            self.write(idf)
