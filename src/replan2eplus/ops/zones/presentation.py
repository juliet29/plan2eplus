
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ops.zones.interfaces import Room
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ezobjects.zone import Zone



def get_zone_surfaces(zone: Zone, surfaces: list[Surface]):
    return [i for i in surfaces if i.zone_name == zone.zone_name]


def assign_zone_surfaces(zones: list[Zone], surfaces: list[Surface]):
    for zone in zones:
        z_surfaces = get_zone_surfaces(zone, surfaces)
        zone.surfaces = z_surfaces
        assert len(zone.surfaces) >= 6
    return zones


def create_zones(idf: IDF, rooms: list[Room]):
    for room in rooms:
        idf.add_geomeppy_block(room.geomeppy_block())

    idf.intersect_match()
    # TODO: use custom exceptions, + use shapely to check what the issues are..

    zones = [Zone(_epbunch=i) for i in idf.get_zones()]
    surfaces = [Surface(i) for i in idf.get_surfaces()]
    updates_zones = assign_zone_surfaces(zones, surfaces)


    return updates_zones, surfaces  # oom_map
