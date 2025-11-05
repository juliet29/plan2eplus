from geomeppy import IDF
from expression.collections import Seq
from replan2eplus.ops.afn.idfobject import IDFAFNSurface
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.afn.user_interface import AFNVentingInput


def handle_venting_inputs(
    idf: IDF, subsurfaces: list[Subsurface], venting_inputs: list[AFNVentingInput]
):
    def handle(venting_input: AFNVentingInput):
        match venting_input.selection:
            case "Doors":
                surfaces = (
                    Seq(subsurfaces)
                    .filter(lambda x: x.is_door)
                    .map(lambda x: x.subsurface_name)
                    .to_list()
                )
            case "Windows":
                surfaces = (
                    Seq(subsurfaces)
                    .filter(lambda x: x.is_window)
                    .map(lambda x: x.subsurface_name)
                    .to_list()
                )

        surface_names = list(surfaces)
        for name in surface_names:
            IDFAFNSurface.update_afn_surface(
                idf,
                name,
                "Venting_Availability_Schedule_Name",
                venting_input.schedule_name,
            )

    for input in venting_inputs:
        handle(input)
