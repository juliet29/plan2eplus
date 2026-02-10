import pytest
from plan2eplus.results.sql import create_result_for_qoi, get_sql_results
from plan2eplus.ezcase.ez import EZ, ep_paths
from plan2eplus.ops.subsurfaces.idfobject import read_subsurfaces
from plan2eplus.paths import DynamicPaths
from plan2eplus.ex.subsurfaces import (
    SubsurfaceInputOutput,
    SubsurfaceInputOutputExamples,
)
from rich import print
from plan2eplus.ex.afn import AFNExampleCases, AFNCaseDefinition


def prep_test_read_total_pressure(example: AFNCaseDefinition):
    input_path = DynamicPaths.afn_examples / example.name
    case = EZ(input_path / ep_paths.idf_name)

    sql = get_sql_results(input_path)
    qoi_result = create_result_for_qoi(sql, "AFN Node Total Pressure")
    print(qoi_result)
    print(create_result_for_qoi(sql, "Site Wind Direction"))
    print(create_result_for_qoi(sql, "AFN Node Wind Pressure"))
    return qoi_result
    # qoi_result = Q


if __name__ == "__main__":
    res = prep_test_read_total_pressure(AFNExampleCases.A_ew)
