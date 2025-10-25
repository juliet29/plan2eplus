from typing import NamedTuple

from replan2eplus.ex.rooms import Rooms
from replan2eplus.ezcase.ez import EZ
from replan2eplus.ops.subsurfaces.user_interfaces import EdgeGroup, SubsurfaceInputs
from dataclasses import dataclass
from replan2eplus.ex.subsurfaces import details


@dataclass
class AFNCaseDefinition:
    base_case = EZ().add_zones(Rooms().two_room_list)
    edge_groups: list[EdgeGroup]
    n_zones_with_two_plus_valid_surfaces: int
    n_zones_in_afn: int

    @property
    def case_with_subsurfaces(self):
        return self.base_case.add_subsurfaces(
            SubsurfaceInputs(self.edge_groups, details)
        )


r1 = Rooms.r1.name
r2 = Rooms.r2.name
N, E, S, W = "north east south west".upper().split()


A_ns = AFNCaseDefinition(
    [
        EdgeGroup.from_tuple_edges(
            [
                (r1, N),
                (r1, S),
                (r2, N),
                (r2, S),
            ],
            "door",
            "Zone_Direction",
        ),
    ],
    2,
    2,
)
# TODO make edge groupds more ergonomic => dont require to spec which is which kind of edge -> figure it out! only details should hamper.. 
# also, can specify edges using north on an interior object.. but i guess thing getting edges from wont do this.. but shouldnt assume is exterior 
A_ew = AFNCaseDefinition(
    [
        EdgeGroup.from_tuple_edges(
            [(W, r1), (r2, E)],
            "door",
            "Zone_Direction",
        ),
        EdgeGroup.from_tuple_edges([(r1, r2)], "door", "Zone_Zone"),
    ],
    2,
    2,
)


B_ne = AFNCaseDefinition(
    [
        EdgeGroup.from_tuple_edges(
            [(W, r1), (N, r1), (N, r2)],
            "door",
            "Zone_Direction",
        )
    ],
    1,
    1,
)


C_n = AFNCaseDefinition(
    [
        EdgeGroup.from_tuple_edges(
            [
                (r1, N),
            ],
            "door",
            "Zone_Direction",
        ),
        EdgeGroup.from_tuple_edges([(r1, r2)], "door", "Zone_Zone"),
    ],
    1,
    0,
)


D = AFNCaseDefinition(
    [
        EdgeGroup.from_tuple_edges(
            [],
            "door",
            "Zone_Direction",
        )
    ],
    0,
    0,
)


class AFNExampleCases:
    # avail zones, afn zone
    # A -> 2 avail zones, 2 afn zones
    # B -> 1 avail zones, 1 afn zone
    # C -> 1 avail zones, 0 afn zones
    # D -> 0 avail zones, 0 afn zones

    A_ns = A_ns
    A_ew = A_ew
    B_ne = B_ne
    C_n = C_n
    D = D

    @property
    def list(self):
        return [self.A_ns, self.A_ew, self.B_ne, self.C_n, self.D]
