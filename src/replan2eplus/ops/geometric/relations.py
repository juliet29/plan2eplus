from geomeppy import IDF

# from replan2eplus.ops.zones.idfobject import IDFZone
# from replan2eplus.ops.subsurfaces.idfobject import read_subsurfaces
from replan2eplus.ops.surfaces.idfobject import IDFSurface

# from replan2eplus.ops.zones.ezobject import Zone
from replan2eplus.ops.surfaces.ezobject import Surface
# from replan2eplus.ops.subsurfaces.utils import re


# def update_zone_relations(idf: IDF, zone: Zone):
#     zone.surface_names =  IDFZone().get_zone_surface_names(idf, zone.zone_name)


def update_surface_relations(idf: IDF, surface: Surface):
    subsurfaces = IDFSurface.get_surface_subsurfaces(idf, surface.surface_name)
    # print(f"subsurfaces for surf: {subsurfaces}")
    if not subsurfaces:
        # print("no subsurfaces -> returning!\n")
        return

    try:
        subsurface_names = [i.Name for i in subsurfaces]
    except AttributeError:
        # print(f"probelem w subsurface!!")
        # a = 1 + 1
        # b = 2 + 2
        raise Exception("subsurf fail")
    surface.subsurfaces = subsurface_names
    return surface
    # subsurface_objs = read_subsurfaces(idf, subsurface_names)
    # [i.create_ezobject([]) for i in subsurface_objs]

    # now need to turn into ez objects..
