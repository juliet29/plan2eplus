import pytest
from replan2eplus.results.sql import create_result_for_qoi, get_sql_results
from replan2eplus.ezcase.ez import EZ, ep_paths
from replan2eplus.ops.subsurfaces.idfobject import read_subsurfaces
from replan2eplus.paths import DynamicPaths
from replan2eplus.ex.subsurfaces import (
    SubsurfaceInputOutput,
    SubsurfaceInputOutputExamples,
)
from rich import print
from replan2eplus.ex.afn import AFNExampleCases, AFNCaseDefinition


def prep_test_read_total_pressure(example: AFNCaseDefinition):
    input_path = DynamicPaths.afn_examples / example.name
    case = EZ(input_path / ep_paths.idf_name)

    sql = get_sql_results(input_path)
    qoi_result = create_result_for_qoi(sql, "AFN Node Total Pressure")
    print(qoi_result)
    print(create_result_for_qoi(sql, "Site Wind Direction"))
    return qoi_result
    # qoi_result = Q


if __name__ == "__main__":
    res = prep_test_read_total_pressure(AFNExampleCases.A_ew)
