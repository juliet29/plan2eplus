from geomeppy import IDF

from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.surfaces.idfobject import IDFSurface


def update_surface_relations(idf: IDF, surface: Surface):
    subsurfaces = IDFSurface.get_surface_subsurfaces(idf, surface.surface_name)
    if not subsurfaces:
        return

    try:
        subsurface_names = [i.Name for i in subsurfaces]
    except AttributeError:
        raise Exception("subsurf fail")
    surface.subsurfaces = subsurface_names
    return surface

