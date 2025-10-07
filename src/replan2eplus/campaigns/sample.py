from replan2eplus.examples.paths import PATH_TO_IDD, PATH_TO_MINIMAL_IDF
from replan2eplus.ezcase.main import EZCase
from replan2eplus.paths import PATH_TO_WEATHER_FILE
from replan2eplus.campaigns.decorator import make_experimental_campaign



@make_experimental_campaign
def run_simple_ezcase(rooms, subsurface_inputs):
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(rooms)
    case.add_subsurfaces(subsurface_inputs)
