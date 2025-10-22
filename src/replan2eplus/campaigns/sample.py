from replan2eplus.examples.paths import PATH_TO_IDD, PATH_TO_MINIMAL_IDF
from replan2eplus.ezcase.main import EZCase
from replan2eplus.ops.subsurfaces.interfaces import Dimension, Location
from replan2eplus.ops.zones.user_interface import Room
from replan2eplus.paths import PATH_TO_WEATHER_FILE
from replan2eplus.campaigns.decorator2 import make_experimental_campaign
from replan2eplus.campaigns.inputs.defn import SampleDef
from replan2eplus.campaigns.inputs.data import make_data_dict
from replan2eplus.ops.subsurfaces.user_interfaces import (
    SubsurfaceInputs,
    Edge,
    Detail,
)
from replan2eplus.paths import CAMPAIGN_TESTS


# TODO: the definition of "run simple ezcase has to match the data dict variables -> can this be assured?"
@make_experimental_campaign(
    SampleDef().definition_dict, make_data_dict(), root_path=CAMPAIGN_TESTS
)
def run_simple_ezcase(rooms, connections, window_dimension, out_path):
    details = {
        "door": Detail(
            window_dimension, Location("mm", "CENTROID", "CENTROID"), "Door"
        ),
        "window": Detail(
            Dimension(1, 2), Location("mm", "CENTROID", "CENTROID"), "Window"
        ),
    }

    ss_input = SubsurfaceInputs(connections, details)

    print("Starting to create case!")
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(rooms)
    case.add_subsurfaces(ss_input)
    case.save_and_run_case(path_=out_path, RUN=False)
    print("Done creating case!")


if __name__ == "__main__":
    run_simple_ezcase("", "", "", "")
