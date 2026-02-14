from plan2eplus.ops.surfaces.idfobject import IDFSurface
from plan2eplus.ops.zones.user_interface import Room
from eppy.bunch_subclass import EpBunch

from plan2eplus.ops.zones.idfobject import IDFZone
from geomeppyupdated import IDF

from utils4plans.lists import chain_flatten

from plan2eplus.ops.zones.utils import get_surfaces_from_zones


def check_valid_room_geom():  # move to helpers..
    pass


def create_zones(idf: IDF, rooms: list[Room] = []):
    def create_ezobjects(zone_obj: EpBunch, zone: IDFZone):
        # TODO this should be a util.. 
        zone_surface_names = [i.Name for i in zone_obj.zonesurfaces if i] # type: ignore # TODO -> better to do get args.. 
        idf_surfaces = IDFSurface.read(idf, zone_surface_names)
        if not idf_surfaces:
            raise Exception("No surfaces found even though zones were found! Likely the key that describes the surfaces in this file has not been implemented.")
        ez_surfaces = [i.create_ezobject() for i in idf_surfaces]
        # TODO: here are skipping the step of idf surface object..
        ez_zone = [zone.create_ezobject(ez_surfaces)]
        return ez_zone

    if rooms:
        check_valid_room_geom()
        for room in rooms:
            idf = room.geomeppyupdated_block.write(idf)
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
