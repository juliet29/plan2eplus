from pydantic import BaseModel, model_validator
from utils4plans.lists import sort_and_group_objects_dict
from pathlib import Path
import yaml

from plan2eplus.geometry.directions import WallNormalNamesList
from plan2eplus.ops.subsurfaces.interfaces import Edge
from plan2eplus.ops.subsurfaces.user_interfaces import EdgeGroup, EdgeGroupType

#
# yaml should be split by edge type -> zone / zone , vs zone / direction
# within those groups, should be further organized based on the last element in each tuple, which indicates the number of the tuple


def capitalize_drns(val: str):
    if val.upper() in WallNormalNamesList:
        return val.upper()
    return val


class LineConfig(BaseModel):
    source: str
    target: str
    detail_ix: int

    @model_validator(mode="before")
    @classmethod
    def from_list(cls, v):
        if isinstance(v, (list, tuple)):
            return {
                "source": capitalize_drns(v[0]),
                "target": capitalize_drns(v[1]),
                "detail_ix": v[2],
            }
        raise Exception("Expected a list or tuple of [source, target, detail_ix!]")

    @property
    def edge(self):
        return Edge(self.source, self.target)


class TypeConfig(BaseModel):
    x: list[LineConfig]
    y: list[LineConfig]

    @property
    def all_lines(self):
        return self.x + self.y

    @property
    def grouped_lines(self):
        res = sort_and_group_objects_dict(self.all_lines, fx=lambda x: x.detail_ix)
        return res

    def get_edge_details(self, type_: EdgeGroupType):
        def handle(detail_ix: str, lines: list[LineConfig]):
            edges = [i.edge for i in lines]
            eg = EdgeGroup(edges, detail_ix, type_)
            return eg

        return [
            handle(detail_ix, lines) for detail_ix, lines in self.grouped_lines.items()
        ]


class EdgesConfig(BaseModel):
    zone_zone: TypeConfig
    zone_direction: TypeConfig

    @property
    def edge_groups(self):
        zone = self.zone_zone.get_edge_details("Zone_Zone")
        zone_drn = self.zone_direction.get_edge_details("Zone_Direction")
        return zone + zone_drn


# TODO: add to utils4plans
def read_yaml(path: Path):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data


def get_edges_from_yaml(path: Path):
    data = read_yaml(path)
    res = EdgesConfig.model_validate(data)
    return res


def create_edge_inputs(path: Path):
    res = get_edges_from_yaml(path)
    return res.edge_groups
