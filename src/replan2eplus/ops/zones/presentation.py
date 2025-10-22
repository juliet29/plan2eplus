from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ops.zones.interfaces import Room

# from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ops.zones.idfobject import Zone
from geomeppy import IDF
from rich import print 


# def get_zone_surfaces(zone: Zone, surfaces: list[Surface]):
#     return [i for i in surfaces if i.zone_name == zone.zone_name]


# def assign_zone_surfaces(zones: list[Zone], surfaces: list[Surface]):
#     for zone in zones:
#         z_surfaces = get_zone_surfaces(zone, surfaces)
#         zone.surfaces = z_surfaces
#         assert len(zone.surfaces) >= 6
#     return zones


def create_zones(idf: IDF, rooms: list[Room]):
    for room in rooms:
        idf = room.geomeppy_block.write(idf)

    idf.intersect_match()
    # TODO: use custom exceptions, + use shapely to check what the issues are..
    zones = Zone.read(idf)
    print(zones)

    # zones = [Zone(_epbunch=i) for i in idf.get_zones()]
    # ## zone.get_referring_objs
    # surfaces = [Surface(i) for i in idf.get_surfaces()]
    # updates_zones = assign_zone_surfaces(zones, surfaces)

    # return updates_zones, surfaces  # oom_map
