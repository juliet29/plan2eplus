from dataclasses import dataclass
from pathlib import Path
from typing import Any
from omegaconf import OmegaConf

#
# yaml should be split by edge type -> zone / zone , vs zone / direction
# within those groups, should be further organized based on the last element in each tuple, which indicates the number of the tuple


@dataclass
class LineConfig:
    source: str
    target: str
    detail_ix: int


@dataclass
class WorkingTypeConfig:
    x: list[LineConfig]
    y: list[LineConfig]


@dataclass
class TypeConfig:
    x: list[list]
    y: list[list]


@dataclass
class EdgesConfig:
    zone_zone: TypeConfig
    zone_direction: TypeConfig


def to_line_config(item: Any):
    if isinstance(item, (list, tuple)):
        return LineConfig(*item)
    raise Exception(f"Expected list or tuple but got {type(item)}")


# def to_type_config


def get_edges_from_yaml(path: Path) -> EdgesConfig:
    input_config = OmegaConf.load(path)
    schema = OmegaConf.structured(EdgesConfig)
    merged_config = OmegaConf.merge(schema, input_config)

    res = OmegaConf.to_object(merged_config)
    return res  # pyright: ignore[reportReturnType]


def to_edge_details():
    pass
