from replan2eplus.examples.paths import PATH_TO_IDD, PATH_TO_MINIMAL_IDF
from replan2eplus.ezcase.main import EZCase
from replan2eplus.ops.zones.interfaces import Room
from replan2eplus.paths import PATH_TO_WEATHER_FILE
from replan2eplus.campaigns.decorator2 import make_experimental_campaign
from replan2eplus.examples.campaigns import SampleDef
from replan2eplus.ops.subsurfaces.interfaces import (
    SubsurfaceInputs,
    Edge,
    Details,
    Dimension,
    Location,
)


@make_experimental_campaign(SampleDef().definition_dict)
def run_simple_ezcase(rooms, edges, edge_detail_map, dimension):
    door_detail = Details(
        Dimension(1, 2), Location("mm", "CENTROID", "CENTROID"), "Door"
    )
    window_detail = Details(dimension, Location("mm", "CENTROID", "CENTROID"), "Window")

    ss_input = SubsurfaceInputs(
        edges, {0: window_detail, 1: door_detail}, edge_detail_map
    )  # TODO: think about how to map.. or better way to define subsurfaces..  -> should be able to pass in a list?

    print("Starting to create case!")
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(rooms)
    case.add_subsurfaces(ss_input)
    print("Done creating case!")


if __name__ == "__main__":
    run_simple_ezcase("", "", "", "")
