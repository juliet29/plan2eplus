import pyprojroot
from utils4plans.paths import StaticPaths


BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
static_paths = StaticPaths("", base_path=BASE_PATH)


class DynamicPaths:
    # TODO: call this somthing ep speciifc, like ep_config
    config = BASE_PATH / "epconfig"

    THROWAWAY_PATH = BASE_PATH / "throwaway"
    results_for_tests = static_paths.models / "results_for_tests"
    trials = static_paths.models / "trials"
    ORTHO_CASE_RESULTS = results_for_tests / "ortho"
    CAMPAIGN_TESTS = results_for_tests / "campaigns"
    subsurface_examples = results_for_tests / "subsurface_examples"
    afn_examples = results_for_tests / "afn_examples"
    airboundary_examples = results_for_tests / "airboundary_examples"
    test_scheds = static_paths.temp / "test_scheds"
    ts_open = test_scheds / "open"
    ts_dynamic = test_scheds / "dynamic"
    ts_closed = test_scheds / "closed"


class Constants:
    # NOTE: these are just for testing, modules that call will have their own names
    idf_name = "out.idf"
    results_location = "results"
    sql_path = "results/eplusout.sql"
    schedule_location = "schedules"


# TODO: put this in config..
SEED = 1234
