from typing import NamedTuple
from pathlib import Path
from plan2eplus.ops.constructions.interfaces import (
    BaseConstructionSet,
    EPConstructionSet,
)
from plan2eplus.paths2 import ep_paths


class ConstructionInput(NamedTuple):
    const_idf_paths: list[Path]
    mat_idf_paths: list[Path]
    construction_set: EPConstructionSet


default_construction_set = EPConstructionSet(
    # interior then exterior
    # TODO should be able to specify a tuple, and just one object if its the same.., trim white space
    wall=BaseConstructionSet("Medium Partitions", "Medium Exterior Wall"),
    floor=BaseConstructionSet("Medium Floor", "Medium Floor"),
    roof=BaseConstructionSet("Medium Roof/Ceiling", "Medium Roof/Ceiling"),
    window=BaseConstructionSet("Sgl Clr 6mm", "Sgl Clr 6mm"),
    door=BaseConstructionSet("Medium Furnishings", "Medium Furnishings"),
)  # TODO -> could one quicly change the names of these?

default_construction_input = ConstructionInput(
    ep_paths.construction_idfs,
    ep_paths.material_idfs,
    default_construction_set,
)
