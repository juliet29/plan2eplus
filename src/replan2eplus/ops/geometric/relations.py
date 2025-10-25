from geomeppy import IDF
from replan2eplus.ops.zones.idfobject import IDFZone
from replan2eplus.ops.subsurfaces.idfobject import IDFSubsurfaceBase
from replan2eplus.ops.surfaces.idfobject import IDFSurface
from replan2eplus.ops.zones.ezobject import Zone
from replan2eplus.ops.surfaces.ezobject import Surface


def update_zone_relations(idf: IDF, zone: Zone):
    idf_zone = IDFZone().get_one_idf_object(idf, zone.zone_name)
    print(idf_zone)
