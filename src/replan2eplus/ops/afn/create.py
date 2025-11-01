from replan2eplus.ops.afn.utils.coefficients import (
    create_pressure_data,
    assign_external_nodes,
)
from replan2eplus.ops.afn.utils.venting import handle_venting_inputs
from replan2eplus.ops.afn.logic import determine_afn_objects
from replan2eplus.ops.afn.user_interface import AFNInput
from replan2eplus.ops.airboundary.ezobject import Airboundary
from replan2eplus.ops.afn.interfaces import AFNWriter
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.zones.ezobject import Zone
from geomeppy import IDF
from replan2eplus.ops.afn.ezobject import AirflowNetwork
# from expression.collections import Seq


def select_afn_objects(
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
):
    afn_zones, afn_surfaces = determine_afn_objects(zones, airboundaries + subsurfaces)

    return AirflowNetwork(afn_zones, afn_surfaces)


def create_afn_objects(
    idf: IDF,
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
    afn_inputs: AFNInput | None = None,
):
    if zones and (subsurfaces or airboundaries):
        afn = select_afn_objects(zones, subsurfaces, airboundaries)
        if not afn.zones:
            return AirflowNetwork([], [])

        zone_names = [i.zone_name for i in afn.zones]
        sub_and_surface_names = [i.name for i in afn.afn_surfaces]
        AFNWriter(zone_names, sub_and_surface_names).write(idf)

        if afn_inputs and afn_inputs.venting:
            handle_venting_inputs(idf, subsurfaces, afn_inputs.venting)
            afn.schedules = [i.schedule_input for i in afn_inputs.venting]
        if afn_inputs and afn_inputs.pressure_coefficients:
            create_pressure_data(
                idf,
                afn_inputs.pressure_coefficients,
            )
            assign_external_nodes(idf, afn.subsurfaces)

        return afn

    return AirflowNetwork([], [])


# TODO: potentially put this under test -> don't init the AFN if didnt find any AFN objects, also add a warning if the afn flag was true.. -> wont be able to access certain output variables
