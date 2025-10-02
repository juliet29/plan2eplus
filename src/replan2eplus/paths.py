import pyprojroot
from utils4plans.paths import StaticPaths


BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
static_paths = StaticPaths("", base_path=BASE_PATH)
THROWAWAY_PATH = BASE_PATH / "throwaway"

TEST_RESULTS = static_paths.models / "results_for_tests"

TWO_ROOM_RESULTS = TEST_RESULTS / "two_room"
TWO_ROOM_AIRBOUNDARY_RESULTS = TEST_RESULTS / "two_room_airboundary"

ORTHO_CASE_RESULTS = TEST_RESULTS / "ortho"

PATH_TO_WEATHER_FILE = (
    static_paths.inputs / "weather/PALO_ALTO/CA_PALO-ALTO-AP_724937_23.EPW"
)
