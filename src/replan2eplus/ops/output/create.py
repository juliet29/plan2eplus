from geomeppy import IDF
from replan2eplus.ops.output.idfobject import IDFOutputSQL, IDFOutputVariable
from replan2eplus.ops.output.defaults import default_variables


def add_output_variables(idf: IDF, variable_names: list[str] = default_variables):
    IDFOutputSQL().check_and_write(idf)
    for name in variable_names:
        IDFOutputVariable(Variable_Name=name).write(idf)
