from typing import Callable
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ezobjects.afn import AirflowNetwork
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.idfobjects.afn import AFNKeys
from replan2eplus.ezobjects.epbunch_utils import get_epbunch_key
from pipe import filter
from rich import print


def get_idf_objects_from_afn_surface_names(
    idf: IDF,
    afn: AirflowNetwork,
    select_fx: Callable[[list[Subsurface]], list[Subsurface]],
):
    subsurfaces = afn.select_afn_subsurfaces(select_fx)
    idf_afn_objects = idf.get_afn_objects()
    idf_afn_surfaces = list(
        idf_afn_objects
        | filter(lambda x: get_epbunch_key(x) == AFNKeys.SURFACE)
        | filter(lambda x: x.Surface_Name in [i.subsurface_name for i in subsurfaces])
    )
    print(idf_afn_surfaces)
    return idf_afn_surfaces


# next update venting schedule for this object..
