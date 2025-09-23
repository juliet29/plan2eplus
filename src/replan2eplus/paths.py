import pyprojroot
from utils4plans.paths import StaticPaths


BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
static_paths = StaticPaths("", base_path=BASE_PATH)
THROWAWAY_PATH = BASE_PATH / "throwaway"
TWO_ROOM_RESULTS = BASE_PATH / "results_for_tests/two_room"

PATH_TO_WEATHER_FILE = (
    static_paths.inputs / "weather/PALO_ALTO/CA_PALO-ALTO-AP_724937_23.EPW"
)
