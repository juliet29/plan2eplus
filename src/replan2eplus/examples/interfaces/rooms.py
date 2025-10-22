from replan2eplus.ops.zones.interfaces import Room
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.range import Range

HEIGHT = 3.00  # m


class Ranges:
    X1 = Range(0, 1)
    X2 = Range(1, 2)
    Y1 = Range(0, 1)


class Domains:
    d1 = Domain(Ranges.X1, Ranges.Y1)
    d2 = Domain(Ranges.X2, Ranges.Y1)


class Rooms:
    r2 = Room(1, "room1", Domains.d2, HEIGHT)
    r1 = Room(0, "room2", Domains.d1, HEIGHT)
