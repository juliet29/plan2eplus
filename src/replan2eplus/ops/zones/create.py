from replan2eplus.ezobjects.base import EpBunch
from replan2eplus.ops.zones.user_interface import Room

# from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ops.zones.idfobject import IDFZone
from replan2eplus.ops.surfaces.idfobject import IDFSurface
from geomeppy import IDF

from utils4plans.lists import chain_flatten

from replan2eplus.ops.zones.utils import get_surfaces_from_zones
# class ZoneAndSurfaces(NamedTuple):
#     pass

# def get_zone_surfaces(zone: Zone, surfaces: list[Surface]):
#     return [i for i in surfaces if i.zone_name == zone.zone_name]


# def assign_zone_surfaces(zones: list[Zone], surfaces: list[Surface]):
#     for zone in zones:
#         z_surfaces = get_zone_surfaces(zone, surfaces)
#         zone.surfaces = z_surfaces
#         assert len(zone.surfaces) >= 6
#     return zones


def check_valid_room_geom(): # move to helpers.. 
    pass


def create_zones(idf: IDF, rooms: list[Room] = []):
    def create_ezobjects(zone_obj: EpBunch, zone: IDFZone):
        a = 1+1 
        
        ez_surfaces = zone_obj.zonesurfaces

        print(ez_surfaces)
        ez_zone = [zone.create_ezobject(ez_surfaces)]
        return ez_zone

    if rooms:
        check_valid_room_geom()
        for room in rooms:
            idf = room.geomeppy_block.write(idf)
        idf.intersect_match()

    zone_objects = IDFZone().get_idf_objects(idf)
    zones = IDFZone.read(idf)
    ez_zones = chain_flatten(
        [create_ezobjects(zo, z) for zo, z in zip(zone_objects, zones)]
    )
    ez_surfaces = get_surfaces_from_zones(ez_zones)

    return ez_zones, ez_surfaces  # NOTE: these have surfaces so can just roll with that ..

    # return zones
    # print(zones)

    # zones = [Zone(_epbunch=i) for i in idf.get_zones()]
    # ## zone.get_referring_objs
    # surfaces = [Surface(i) for i in idf.get_surfaces()]
    # updates_zones = assign_zone_surfaces(zones, surfaces)

    # return updates_zones, surfaces  # oom_map
