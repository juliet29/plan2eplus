from typing import Literal
from pydantic import BaseModel, RootModel, field_validator
from pathlib import Path

from plan2eplus.io.edges import read_yaml
from plan2eplus.ops.subsurfaces.interfaces import Dimension, Location, SubsurfaceType


class SubsurfaceConfig(BaseModel):
    dimension: Dimension
    location: Location
    type_: SubsurfaceType

    @field_validator("type_", mode="before")
    @classmethod
    def normalize_type(cls, v):
        if isinstance(v, str):
            return v.capitalize()
        return v


class AirboundaryConfig(BaseModel):
    type_: Literal["airboundary"]


class DetailsConfig(RootModel):
    root: dict[int | str, SubsurfaceConfig | AirboundaryConfig]


def get_details_from_yaml(path: Path):
    data = read_yaml(path)
    return DetailsConfig.model_validate(data)
    # door = data[1]
    # return SubsurfaceConfig.model_validate(door)
