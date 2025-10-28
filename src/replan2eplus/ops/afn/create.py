from replan2eplus.ops.afn.idfobject import IDFAFNSurface, IDFAFNZone
from replan2eplus.ops.afn.logic import determine_afn_objects
from replan2eplus.ops.airboundary.ezobject import Airboundary
from replan2eplus.ops.afn.interfaces import AFNWriter
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.zones.ezobject import Zone
from geomeppy import IDF
from replan2eplus.ops.afn.ezobject import AirflowNetwork
from expression.collections import Seq


# def find_existing_afn_objects(
#     idf: IDF,
#     zones: list[Zone],
#     subsurfaces: list[Subsurface],
#     airboundaries: list[Airboundary],
#     # surfaces: list[Surface],
# ):
#     afn_zones = (
#         Seq(zones)
#         .filter(
#             lambda x: x.zone_name
#             in Seq(IDFAFNZone.read(idf)).map(lambda x: x.Zone_Name)
#         )
#         .to_list()
#     )
#     afn_surfaces = (
#         Seq(subsurfaces + airboundaries)
#         .filter(
#             lambda x: x.name
#             in Seq(IDFAFNSurface.read(idf)).map(lambda x: x.Surface_Name)
#         )
#         .to_list()
#     )


def select_afn_objects(
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
    # surfaces: list[Surface],
):
    afn_zones, afn_surfaces = determine_afn_objects(zones, airboundaries + subsurfaces)

    zone_names = [i.zone_name for i in afn_zones]
    sub_and_surface_names = [i.name for i in afn_surfaces]

    # TODO: AFN is empty for now -> things that call on it need to take surfaces and sub surfaces together
    return AirflowNetwork(afn_zones, afn_surfaces), AFNWriter(
        zone_names, sub_and_surface_names
    )


def create_afn_objects(
    idf: IDF,
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
):
    airflow_network, afn_writer = select_afn_objects(zones, subsurfaces, airboundaries)
    afn_writer.write(idf)
    return airflow_network
