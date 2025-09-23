from geomeppy import IDF as geomeppyIDF
from replan2eplus.idfobjects.variables import OutputVariables


def request_sql(idf: geomeppyIDF):
    if not idf.idfobjects["OUTPUT:SQLITE"]:
        obj = idf.newidfobject("OUTPUT:SQLITE")
        obj.Option_Type = "Simple"

    return idf


def check_existing_variable(idf: geomeppyIDF, new_var_name):
    var_names = [o.Variable_Name for o in idf.idfobjects["OUTPUT:VARIABLE"]]
    if new_var_name in var_names:
        return True


def is_surface_or_zone_wind(name):
    if "Wind" in name: # Wind variables only report hourly? how about other variables? # TODO check if this is needed.. 
        if "Zone" in name or "Surace" in name:
            return True


def add_output_variable(idf: geomeppyIDF, name: str, reporting_frequency="Timestep"):
    if check_existing_variable(idf, name):
        return idf

    if is_surface_or_zone_wind(name):
        reporting_frequency = "Hourly"

    obj = idf.newidfobject("OUTPUT:VARIABLE")
    obj.Key_Value = "*"
    obj.Variable_Name = name
    obj.Reporting_Frequency = reporting_frequency
    return idf


def request_output_variables(idf: geomeppyIDF, variables: list[OutputVariables]):
    for var in variables:
        idf = add_output_variable(idf, var)

    return idf
