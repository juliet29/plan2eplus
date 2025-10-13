from replan2eplus.geometry.domain import Domain
from replan2eplus.idfobjects.subsurface import SubsurfaceObject
from replan2eplus.ops.subsurfaces.interfaces import (
    ZoneEdge,
    ZoneDirectionEdge,
    Detail,
    Location,
    SubsurfaceInputs,
    Dimension,
    EdgeGroup,
    SubsurfaceInputs2,
)
from replan2eplus.examples.cases.minimal import get_minimal_case_with_rooms, test_rooms
from replan2eplus.geometry.directions import WallNormal
from dataclasses import dataclass
from replan2eplus.ezobjects.subsurface import Edge

FACTOR = 4

room1, room2 = test_rooms

val = 0.5
random_surface_name = "Block `room1` Storey 0 Wall 0003"
subsurface_object = SubsurfaceObject("Test", random_surface_name, val, val, val, val)


# TODO probably a good idea to put these in classes..?
zone_edge = ZoneEdge(room1.name, room2.name)
zone_drn_edge = ZoneDirectionEdge(room1.name, WallNormal.WEST)
zone_drn_edge_room2 = ZoneDirectionEdge(room2.name, WallNormal.EAST)

location = Location("mm", "SOUTH_WEST", "SOUTH_WEST")
location_bl = Location("bm", "WEST", "WEST")

assert isinstance(room1.domain, Domain)
dimension = Dimension(
    room1.domain.horz_range.size / FACTOR, room1.domain.vert_range.size / FACTOR
)

door_details = Detail(dimension, location, "Door")
window_details = Detail(dimension, location, "Window")
window_details_bl = Detail(dimension, location_bl, "Window")

details = {
    "door": Detail(dimension, location, "Door"),
    "window": Detail(dimension, location_bl, "Window"),
    "window_bl": Detail(dimension, location_bl, "Window"),
}


# testing actual implementation..



e0 = Edge(room1.name, room2.name)
e1 = Edge(room1.name, "WEST")
e2 = Edge(room1.name, "NORTH")
e3 = Edge(room2.name, "SOUTH")



#TODO: think about how to input edge groups with combined types.. 
edge_groups = {
    "door": [EdgeGroup.from_tuple_edges([e0], "door", "Zone_Zone")],
    "window": [
        EdgeGroup.from_tuple_edges(
            [e1],
            "window",
            "Zone_Direction",
        )
    ],
    "ns_windows": [EdgeGroup.from_tuple_edges([e2, e3], "window", "Zone_Direction")],
    "windows": [EdgeGroup.from_tuple_edges([e1, e2, e3], "window", "Zone_Direction")],
    "window_bl": [EdgeGroup.from_tuple_edges([e1], "window_bl", "Zone_Direction")],
}


subsurface_inputs_dict = {
    "interior": SubsurfaceInputs2(
        edge_groups["door"],
        details,
    ),
    "simple": SubsurfaceInputs2(edge_groups["door"] + edge_groups["window"], details),
    "airboundary": SubsurfaceInputs2(
        edge_groups["door"] + edge_groups["ns_windows"], details
    ),
    "three_details": SubsurfaceInputs2(
        edge_groups["door"] + edge_groups["window_bl"] + edge_groups["ns_windows"],
        details,
    ),
}


def get_minimal_case_with_subsurfaces():
    case = get_minimal_case_with_rooms()
    case.add_subsurfaces(subsurface_inputs_dict["simple"])
    return case
