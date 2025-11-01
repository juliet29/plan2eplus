from replan2eplus.ex.afn import AFNEdgeGroups, AFNExampleCases
from replan2eplus.ex.make import make_test_case, airboundary_edges
from replan2eplus.ex.subsurfaces import (
    SubsurfaceInputOutput,
    SubsurfaceInputOutputExamples,
)
from replan2eplus.paths import DynamicPaths
import sys


def write_subsurface_cases_to_file(example: SubsurfaceInputOutput):
    output_path = DynamicPaths.subsurface_examples / example.info.name
    case = make_test_case(example.edge_groups, afn=True, output_path=output_path)
    case.save_and_run(run=False)


def write_afn_cases_to_file(run=False):
    ae = AFNExampleCases()
    examples = ae.list
    # examples = [ae.C_n]
    for example in examples:
        output_path = DynamicPaths.afn_examples / example.name
        case = make_test_case(example.edge_groups, afn=True, output_path=output_path)
        case.save_and_run(run=run)


def write_airboundary_case_to_file():
    example = SubsurfaceInputOutputExamples.airboundary
    output_path = DynamicPaths.airboundary_examples / example.info.name
    case = make_test_case(
        example.edge_groups, airboundary_edges, afn=True, output_path=output_path
    )
    case.save_and_run(run=False)


if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     run_case: bool = bool(sys.argv[1])
    # else:
    #     run_case = False
    write_afn_cases_to_file(run=False)
