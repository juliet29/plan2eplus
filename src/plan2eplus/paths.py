import pyprojroot
from utils4plans.paths import StaticPaths


BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
static_paths = StaticPaths("", base_path=BASE_PATH)

CONFIG_PATH = BASE_PATH / "epconfig"


class Constants:
    # NOTE: these are just for testing, modules that call will have their own names
    idf_name = "out.idf"
    results_location = "results"
    sql_path = "results/eplusout.sql"
    schedule_location = "schedules"


# TODO: put this in config..
SEED = 1234
