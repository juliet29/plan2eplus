from typing import Callable
from replan2eplus.ezobjects.base import EpBunch
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ezobjects.afn import AirflowNetwork
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.idfobjects.afn import AFNKeys
from replan2eplus.ezobjects.epbunch_utils import get_epbunch_key
from pipe import filter
from rich import print
from replan2eplus.ops.schedule.interfaces import ScheduleInput
from replan2eplus.ops.schedule.presentation import create_schedule


def get_idf_objects_from_afn_surface_names(
    idf: IDF,
    afn: AirflowNetwork,
    select_fx: Callable[[list[Subsurface]], list[Subsurface]],
):
    subsurfaces = afn.select_afn_subsurfaces(select_fx)
    idf_afn_objects = idf.get_afn_objects()
    idf_afn_surfaces: list[EpBunch] = list(
        idf_afn_objects
        | filter(lambda x: get_epbunch_key(x) == AFNKeys.SURFACE)
        | filter(lambda x: x.Surface_Name in [i.subsurface_name for i in subsurfaces])
    )
    # print(idf_afn_surfaces)
    return idf_afn_surfaces


def update_idf_afn_surfaces_vent_schedule(
    idf: IDF,
    idf_afn_surfaces: list[EpBunch],
    vent_schedule: ScheduleInput,
):
    # TODO this should all be in presentation for schedule..
    create_schedule(idf, vent_schedule)

    for surface in idf_afn_surfaces:
        surface.Ventilation_Control_Mode = "Constant"
        surface.Venting_Availability_Schedule_Name = vent_schedule.name
    return idf


# TODO this should exisr on the case -> so it passes in the early stuff.. OR it should take in a case -> TODO define priorities for all..
def update_vent_schedule_for_select_afn_surfaces(
    idf: IDF,
    afn: AirflowNetwork,
    select_fx: Callable[[list[Subsurface]], list[Subsurface]],
    vent_schedule: ScheduleInput,
):
    idf_afn_surfaces = get_idf_objects_from_afn_surface_names(idf, afn, select_fx)
    return update_idf_afn_surfaces_vent_schedule(idf, idf_afn_surfaces, vent_schedule)

    # pass
    # if vent schedule not in idf, add
    # add vent sched name to all objects


# next update venting schedule for this object..
