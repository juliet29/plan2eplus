from dataclasses import dataclass
from utils4plans.sets import set_intersection
from typing import NamedTuple, Literal, TypeVar, Union
from replan2eplus.ezobjects.subsurface import Edge
from replan2eplus.geometry.contact_points import CornerEntries, CardinalEntries
from replan2eplus.geometry.directions import WallNormal, WallNormalNamesList
from replan2eplus.geometry.nonant import NonantEntries

ContactEntries = Union[CornerEntries, CardinalEntries, Literal["CENTROID"]]


class Dimension(NamedTuple):
    width: float
    height: float

    @property
    def as_tuple(self):
        return (self.width, self.height)


class ZoneDirectionEdge(NamedTuple):
    """for convenience, spaces are described using room names, not the idf names"""

    space_a: str
    space_b: WallNormal


class ZoneEdge(NamedTuple):
    """for convenience, spaces are described using room names, not the idf names"""

    space_a: str
    space_b: str


class Location(NamedTuple):
    nonant_loc: NonantEntries
    nonant_contact_loc: ContactEntries
    subsurface_contact_loc: ContactEntries

    # TODO make some defaults!


class Details(NamedTuple):
    dimension: Dimension
    location: Location
    type_: Literal["Door", "Window"]


def flatten_dict_map(dict_map: dict[int, list[int]]) -> list[tuple[int, int]]:
    res = []
    for k, v in dict_map.items():
        res.extend([(k, input) for input in v])
    return res


class IndexPair(NamedTuple):
    detail_ix: int
    edge_ix: int


T = TypeVar("T")


@dataclass
class EdgeGroup:
    edges: list[Edge]
    detail: Details | str 
    type_: Literal["Zone_Direction", "Zone_Zone"]

    def __post_init__(self):
        self.edges_match_type_()

    @classmethod
    def from_tuple_edges(
        cls,
        edges_: list[tuple[str, str]],
        detail: Details|str,
        type_: Literal["Zone_Direction", "Zone_Zone"],
    ):
        edges = [Edge(*i) for i in edges_]
        return cls(edges, detail, type_)

    # these should all have the same type of edges => either zone_edge or zone_direction edges..
    def edges_match_type_(self):
        for edge in self.edges:
            if self.type_ == "Zone_Direction":
                assert len(set_intersection(edge.as_tuple, WallNormalNamesList)) == 1, (
                    f"Invalid `Zone_Direction` Edge: {edge}"
                )
            else:
                assert len(set_intersection(edge.as_tuple, WallNormalNamesList)) == 0, (
                    f"Invalid `Zone_Zone` Edge: {edge}"
                )


@dataclass
class SubsurfaceInputs2:
    edge_groups: list[EdgeGroup]


class SubsurfaceInputs:
    edges: dict[int, Edge]
    details: dict[int, Details]
    map_: (
        dict[int, list[int]] | list[IndexPair]
    )  # TODO -> is there a better way to do this?
    # they key here is the detail, and the values are the edge indices..

    @property
    def _index_pairs(self):
        if not isinstance(self.map_, list):
            flattened_map = flatten_dict_map(self.map_)
            return (IndexPair(*i) for i in flattened_map)
        return self.map_

    @property
    def _zone_edges(self):
        return {
            k: ZoneEdge(*v) for k, v in self.edges.items() if not v.is_directed_edge
        }

    @property
    def _zone_drn_edges(self):
        return {
            k: ZoneDirectionEdge(*v.sorted_directed_edge)
            for k, v in self.edges.items()
            if v.is_directed_edge
        }

    def _replace_indices(self, edge_dict: dict[int, T]):
        return [
            (edge_dict[i.edge_ix], self.details[i.detail_ix])
            for i in self._index_pairs
            if i.edge_ix in edge_dict.keys()
        ]

    @property
    def zone_pairs(self):
        return self._replace_indices(self._zone_edges)

    @property
    def zone_drn_pairs(self):
        return self._replace_indices(self._zone_drn_edges)
