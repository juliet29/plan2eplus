from geomeppy import IDF
from replan2eplus.ops.output.idfobject import IDFOutputSQL, IDFOutputVariable
from replan2eplus.ops.output.defaults import default_variables


def add_output_variables(
    idf: IDF,
    additional_variables: list[str] = [],
    variable_names: list[str] = default_variables,
):
    # TODO: ideaelly can check if the additional variables are legitimate..
    IDFOutputSQL().check_and_write(idf)
    for name in variable_names + additional_variables:
        IDFOutputVariable(Variable_Name=name).check_and_write(idf)
