from replan2eplus.ezobjects.base import EpBunch
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.zones.user_interface import Room

from replan2eplus.ops.zones.idfobject import IDFZone
from geomeppy import IDF

from utils4plans.lists import chain_flatten

from replan2eplus.ops.zones.utils import get_surfaces_from_zones


def check_valid_room_geom():  # move to helpers..
    pass


def create_zones(idf: IDF, rooms: list[Room] = []):
    def create_ezobjects(zone_obj: EpBunch, zone: IDFZone):
        surface_objs: list[EpBunch] = zone_obj.zonesurfaces  # type: ignore
        ez_zone = [zone.create_ezobject([Surface(i) for i in surface_objs])]
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

    return (
        ez_zones,
        ez_surfaces,
    )  
