from expression.collections import Seq
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.zones.ezobject import Zone


def get_avail_zones(zones: list[Zone]):
    return Seq(zones).filter(lambda x: len(x.subsurface_names) > 2)
