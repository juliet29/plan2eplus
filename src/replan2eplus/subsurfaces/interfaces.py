from typing import NamedTuple, Literal
from dataclasses import dataclass
from utils4plans.sets import set_difference
from replan2eplus.geometry.contact_points import CornerEntries
from replan2eplus.geometry.directions import WallNormal
from replan2eplus.geometry.domain_create import Dimension
from replan2eplus.geometry.nonant import NonantEntries


# class Node(NamedTuple):
#     name: str # needs to be in zone_plan_dict.. => so either post init or validate later..
#     type_: Literal["Zone", "Direction"]


# class Edge(NamedTuple):
#     u: Node
#     v: Node


class ZoneDirectionEdge(NamedTuple):
    u: str
    v: WallNormal

class ZoneEdge(NamedTuple):
    u: str
    v: str


# @dataclass
# class Edges:
#     edges: list[ZoneEdge | ZoneDirectionEdge]

#     @property
#     def zone_edges(self):
#         return [i for i in self.edges if i.u.type_ == "Zone" and i.v.type_ == "Zone"]

#     @property
#     def zone_drn_edges(self):
#         # TODO: sort and give type..
#         return set_difference(self.edges, self.zone_edges)
    



class Location(NamedTuple):
    nonant_loc: NonantEntries
    nonant_contact_loc: CornerEntries
    subsurface_contact_loc: CornerEntries
    

# class Attributes:
#     pass

class Details(NamedTuple):
    # edge: Edge
    dimension: Dimension
    location: Location
    type_: Literal["Door", "Window"]
    # TODO "Door:Interzone" is also a possibility..  -> IDF and the subsurface do not shar the interface, but they do match.. 
