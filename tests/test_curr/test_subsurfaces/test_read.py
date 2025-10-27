import pytest
from replan2eplus.ezcase.ez import EZ, ep_paths
from replan2eplus.ops.subsurfaces.idfobject import read_subsurfaces
from replan2eplus.paths import DynamicPaths
from replan2eplus.ex.subsurfaces import (
    SubsurfaceInputOutput,
    SubsurfaceInputOutputExamples,
)
from replan2eplus.ex.make import make_test_case


def write_subsurface_cases_to_file(example: SubsurfaceInputOutput):
    output_path = DynamicPaths.subsurface_examples / example.info.name
    case = make_test_case(example.edge_groups, output_path=output_path)
    case.save_and_run(run=False)


def prep_test_read_subsurfaces(example: SubsurfaceInputOutput):
    input_path = DynamicPaths.subsurface_examples / example.info.name
    case = EZ(input_path / ep_paths.idf_name)
    subsurfs = read_subsurfaces(case.idf)
    assert len(subsurfs) == example.info.sum_subsurfaces


@pytest.mark.parametrize("example", SubsurfaceInputOutputExamples().list_examples)
def test_read_subsurfaces(example):
    prep_test_read_subsurfaces(example)


if __name__ == "__main__":
    examples = SubsurfaceInputOutputExamples()
    for ex in examples.list_examples:
        test_read_subsurfaces(ex)
