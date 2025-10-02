from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.range import Range
from replan2eplus.ops.zones.interfaces import OrthoDomain, Room
from replan2eplus.examples.minimal import get_minimal_case
from rich import print

ORTHO_COORDS = [(1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (1, 3)]
HEIGHT = 3
ortho_room = Room(0, "ortho", OrthoDomain.from_tuple_list(ORTHO_COORDS), HEIGHT)
rect_room = Room(1, "rect", Domain(Range(2, 3), Range(1, 2)), HEIGHT)

def create_ortho_plan():
    case = get_minimal_case()
    case.add_zones([ortho_room, rect_room])
    return case
    


if __name__ == "__main__":
    res = create_ortho_plan()
    # print(res.zones)
    print(res.zones[0].surfaces)
    # print(res.zones)